import random
import os
import pygame
from datetime import datetime
from models import Combattant
from attaques import (
    executer_attaque, obtenir_attaques_disponibles, gerer_cooldown_attaque
)
from items import obtenir_item, test_item_giver
from event_effect import verifier_effet_items
import events
from db_init import get_db
from utils import (
    menu_principale_de_combat, afficher_etat_combat, 
    afficher_intro_combat, afficher_tour, afficher_resultat_combat,
    afficher_equipe, choix_perso, choisir_nom_joueur
)

db = get_db()

class Partie:
    def __init__(self):
        self.equipe = []
        self.personnages_dispo = []
        self.heros_choisis = 0
        self.monstres = []
        self.monstre_actuel_index = 0
        self.tour = 1
        self.tours_cumule = 0  # Compteur total des tours sur toute la partie
        self.nom_joueur = ""
        self.victoires = 0
        self.items_par_rarete = {}
        self.raretes = {}
        # Config: item de départ (None pour désactiver). Peut être défini par code.
        # Par défaut, on donne la Cape du héro pour vos tests.
        self.start_item_name = os.getenv("DEBUG_ITEM_START", "Bouclier du gardien")
        self.start_item_trigger_event = True
        
        # État du combat
        self.hero_actuel_index = 0  # Pour gérer quel héro attaque
        self.attaque_choisie = None  # Stocker l'attaque sélectionnée
        
        # Config fenêtre et rendu scalable
        pygame.init()
        # Résolution logique de référence
        self.BASE_WIDTH = 1600
        self.BASE_HEIGHT = 900
        # Dimensions logiques utilisées par le reste du jeu
        self.WIDTH = self.BASE_WIDTH
        self.HEIGHT = self.BASE_HEIGHT

        # Fenêtre redimensionnable aux dimensions de l'écran actuel
        display_info = pygame.display.Info()
        initial_w = display_info.current_w
        initial_h = display_info.current_h
        self.screen = pygame.display.set_mode((initial_w, initial_h), pygame.RESIZABLE)
        pygame.display.set_caption("Quest Heroes")

        # Surface de rendu à la résolution logique, qui sera ensuite upscalée/downscalée
        self.base_surface = pygame.Surface((self.BASE_WIDTH, self.BASE_HEIGHT)).convert()
        self._mouse_get_pos_original = pygame.mouse.get_pos

        self.clock = pygame.time.Clock()
        self.running = True

        # Ecran actuel (menu par défaut)
        from screens.menu import Menu
        self.current_screen = Menu(self)

    def set_start_item(self, item_name, trigger_event=True):
        """Définit l'item donné automatiquement au début du combat."""
        self.start_item_name = item_name
        self.start_item_trigger_event = trigger_event
        
    def run(self):
        while self.running:
            event_list = pygame.event.get()
            # Mettre à jour les facteurs d'échelle selon la taille réelle de la fenêtre
            screen_w, screen_h = self.screen.get_size()
            scale_x = self.BASE_WIDTH / max(1, screen_w)
            scale_y = self.BASE_HEIGHT / max(1, screen_h)

            # Recaler les événements souris sur la résolution logique
            for ev in event_list:
                if hasattr(ev, "pos"):
                    lx = int(ev.pos[0] * scale_x)
                    ly = int(ev.pos[1] * scale_y)
                    ev.pos = (lx, ly)
                    ev.dict["pos"] = (lx, ly)
                if hasattr(ev, "x") and hasattr(ev, "y") and ev.type == pygame.MOUSEWHEEL:
                    # Pygame 2 fournit x/y pour wheel; pos déjà recadrée au-dessus si dispo
                    pass

            # Monkey-patch pour les appels directs à pygame.mouse.get_pos() dans les écrans
            def _logical_mouse_pos():
                rx, ry = self._mouse_get_pos_original()
                return (int(rx * scale_x), int(ry * scale_y))
            pygame.mouse.get_pos = _logical_mouse_pos
            for event in event_list:
                if event.type == pygame.QUIT:
                    self.running = False

            # UPDATE
            self.current_screen.update()

            # EVENTS - Correction : passer event_list au lieu du module events
            self.current_screen.handle_events(event_list)
            
            # DRAW sur la surface logique puis upscale vers l'écran
            self.base_surface.fill((30, 30, 30))
            self.current_screen.draw(self.base_surface)

            scaled = pygame.transform.smoothscale(self.base_surface, (screen_w, screen_h))
            self.screen.blit(scaled, (0, 0))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def change_screen(self, new_screen_class):
        """Change l'écran actuel"""
        self.current_screen = new_screen_class(self)
        
    def choisir_equipe(self):
        """Initialise la sélection d'équipe (appelé depuis l'écran de sélection)"""
        self.personnages_dispo = list(db.personnages.find())
        self.equipe = []
        self.heros_choisis = 0

    def selectionner_hero(self, index):
        """Sélectionne un héros depuis la liste disponible"""
        if self.heros_choisis >= 3:
            return False  # déjà 3 héros choisis

        if index < 0 or index >= len(self.personnages_dispo):
            return False

        perso_choisi = self.personnages_dispo.pop(index)
        self.equipe.append(Combattant(perso_choisi, est_heros=True))
        self.heros_choisis += 1
        return True

    def deselectionner_hero(self, index):
        """Retire un héros sélectionné et le remet dans la liste disponible"""
        if self.heros_choisis <= 0:
            return False

        if index < 0 or index >= len(self.equipe):
            return False

        hero_retire = self.equipe.pop(index)
        if hasattr(hero_retire, "_raw_data"):
            self.personnages_dispo.append(hero_retire._raw_data)
        else:
            self.personnages_dispo.append({
                "nom": hero_retire.nom,
                "atk": hero_retire.atk,
                "def": hero_retire.defense,
                "pv_max": hero_retire.pv_max,
                "classe": getattr(hero_retire, "classe", ""),
                "attaques": getattr(hero_retire, "attaques", []),
                "description": getattr(hero_retire, "description", ""),
            })

        self.heros_choisis -= 1
        return True

    def equipes_pretes(self):
        """Vérifie si l'équipe est complète"""
        return self.heros_choisis == 3
        
    def charger_monstres(self):
        """Charge tous les monstres depuis la DB en préservant leurs données (lieu, message_intro)"""
        monstres_data = list(db.monstres.find())
        self.monstres = []
        for monstre_data in monstres_data:
            combattant = Combattant(monstre_data, est_heros=False)
            # Préserver les infos d'ambiance
            combattant.lieu = monstre_data.get("lieu", "menu")
            combattant.message_intro = monstre_data.get("message_intro", "Vous vous préparez au combat...")
            self.monstres.append(combattant)
            
    def charger_items(self):
        """Charge tous les items depuis la DB"""
        # Charger les taux de rareté
        self.raretes = {'commun': 40, 'peu_commun': 30, 'rare': 20, 'legendaire': 10}

        # Charger tous les items
        items = list(db.items.find({}, {"_id": 0}))

        # Regrouper par rareté
        items_par_rarete = {}
        for item in items:
            r = item["rarete"]
            if r not in items_par_rarete:
                items_par_rarete[r] = []
            items_par_rarete[r].append(item)

        self.items_par_rarete = items_par_rarete
    
    def obtenir_monstre_actuel(self):
        """Retourne le monstre actuel du combat"""
        if 0 <= self.monstre_actuel_index < len(self.monstres):
            return self.monstres[self.monstre_actuel_index]
        return None
    
    def monstre_suivant(self):
        """Passe au monstre suivant"""
        self.monstre_actuel_index += 1
        # Repartir au tour 1 pour le nouveau combat, mais garder le cumul global
        self.tour = 1
        self.hero_actuel_index = 0  # Reset l'index du héro actuel
        return self.obtenir_monstre_actuel()
    
    def verifier_focus(self, equipe):
        """Vérifie si un héros a un effet de focus (attire les attaques)"""
        for hero in equipe:
            if hero.est_vivant() and hero.est_cible:
                return hero
        return None
    
    def tour_hero_unique(self, hero, monstre, type_attaque, attaque_info):
        """
        Gère le tour d'un seul héros avec une attaque spécifique
        Version GUI : l'attaque est déjà choisie par le joueur
        """
        resultat = {
            "messages": [],
            "degats": 0,
            "monstre_vivant": monstre.est_vivant(),
            "hero_ko": False
        }

        # Déclencher l'événement start_turn pour les items qui l'écoutent
        events.trigger("start_turn", hero, monstre, self.equipe)

        # Appliquer les effets de statut du héros
        hero.appliquer_status()

        # Si le héros est tombé à 0 PV à cause d'un statut, il ne peut pas agir
        if not hero.est_vivant():
            resultat["hero_ko"] = True
            resultat["messages"].append(f"{hero.nom} succombe à ses effets !")
            return resultat
        
        if not hero.peut_attaquer:
            resultat["messages"].append(f"{hero.nom} ne peut pas attaquer ce tour.")
            return resultat

        # Message d'utilisation de l'attaque (EN PREMIER)
        nom_attaque = attaque_info.get('nom', 'attaque inconnue')
        resultat["messages"].append(f"{hero.nom} utilise {nom_attaque} !")
        
        # Exécution de l'attaque (retourne maintenant un dict avec degats + messages)
        resultat_attaque = executer_attaque(hero, monstre, self.equipe, type_attaque, attaque_info)
        
        # CORRECTION : Vérifier si c'est une métamorphose qui demande une sélection
        if resultat_attaque.get("selection_forme"):
            # Retourner directement le résultat de métamorphose avec tous ses flags
            resultat_attaque["monstre_vivant"] = monstre.est_vivant()
            resultat_attaque["hero_ko"] = False
            return resultat_attaque
        
        degats_infliges = resultat_attaque["degats"]
        messages_effets = resultat_attaque.get("messages", [])
        
        resultat["degats"] = degats_infliges
        
        # Ajouter les messages des effets (saignement, poison, totem, etc.)
        resultat["messages"].extend(messages_effets)
        
        # Message des dégâts infligés
        if degats_infliges > 0:
            resultat["messages"].append(f"> {degats_infliges} dégâts infligés à {monstre.nom} !")
        # Vérifier si le monstre est mort
        if not monstre.est_vivant():
            resultat["messages"].append(f"{monstre.nom} est mort !")

        # Gestion du cooldown
        gerer_cooldown_attaque(hero, type_attaque, attaque_info)

        # Déclencher l'événement end_turn pour les items qui l'écoutent
        events.trigger("end_turn", hero, monstre, self.equipe)

        # Mettre à jour si le monstre est encore vivant
        resultat["monstre_vivant"] = monstre.est_vivant()

        return resultat
    def tour_heros_complet(self, monstre):
        """
        Gère le tour de TOUS les héros automatiquement
        Utilisé pour l'IA ou le mode auto
        """
        messages = []
        degats_totaux = 0

        for hero in self.equipe:
            if not hero.est_vivant():
                continue
            if not monstre.est_vivant():
                break

            # Obtenir les attaques disponibles
            attaques_dispo = obtenir_attaques_disponibles(hero)
            if not attaques_dispo:
                continue
                
            # Choix automatique : première attaque disponible
            type_attaque, attaque_info = attaques_dispo[0]
            
            resultat = self.tour_hero_unique(hero, monstre, type_attaque, attaque_info)
            degats_totaux += resultat["degats"]
            messages.extend(resultat["messages"])

        # Réduire tous les cooldowns à la fin du tour de l'équipe
        for hero in self.equipe:
            hero.reduire_cooldowns()

        return {
            "messages": messages, 
            "degats_totaux": degats_totaux, 
            "monstre_vivant": monstre.est_vivant()
        }
    
    def executer_attaque_hero(self, hero_index, type_attaque):
        """
        Exécute l'attaque d'un héros spécifique
        Appelé depuis l'interface graphique de combat
        """
        if hero_index < 0 or hero_index >= len(self.equipe):
            return {"erreur": "Héros invalide"}
        
        hero = self.equipe[hero_index]
        monstre = self.obtenir_monstre_actuel()
        
        if not hero.est_vivant():
            return {"erreur": f"{hero.nom} est K.O."}
        
        if not monstre or not monstre.est_vivant():
            return {"erreur": "Pas de monstre à attaquer"}
        
        # Vérifier le cooldown
        if hero.cooldowns.get(type_attaque, 0) > 0:
            return {"erreur": f"L'attaque {type_attaque} est en cooldown ({hero.cooldowns[type_attaque]} tours)"}
        
        # Obtenir l'attaque info
        attaques_dispo = obtenir_attaques_disponibles(hero)
        attaque_info = None
        for t, info in attaques_dispo:
            if t == type_attaque:
                attaque_info = info
                break
        
        if not attaque_info:
            return {"erreur": "Attaque non disponible"}
        
        # Exécuter l'attaque
        return self.tour_hero_unique(hero, monstre, type_attaque, attaque_info)

    def tour_monstre(self, monstre):
        """Gère le tour d'attaque du monstre"""
        messages = []
        degats_total = 0
        
        if not monstre.est_vivant():
            return {"messages": messages, "degats_total": degats_total}

        # Appliquer les effets de statut du monstre
        monstre.appliquer_status()

        # Si les statuts tuent le monstre, il ne joue pas son tour
        if not monstre.est_vivant():
            messages.append(f"{monstre.nom} succombe à ses effets !")
            return {"messages": messages, "degats_total": degats_total}
        
        if not monstre.peut_attaquer:
            messages.append(f"{monstre.nom} ne peut pas attaquer ce tour.")
            return {"messages": messages, "degats_total": degats_total}

        cibles_vivantes = [h for h in self.equipe if h.est_vivant()]
        if not cibles_vivantes:
            return {"messages": messages, "degats_total": degats_total}

        # Vérifier si un héros a l'effet focus
        cible_focus = self.verifier_focus(self.equipe)
        cible = cible_focus if cible_focus else random.choice(cibles_vivantes)

        degats = monstre.atk
        degats_reels = cible.prendre_degats(degats)
        degats_total += degats_reels

        if cible_focus:
            messages.append(f"{monstre.nom} attaque {cible.nom} (focus) pour {degats_reels} dégâts")
        else:
            messages.append(f"{monstre.nom} attaque {cible.nom} pour {degats_reels} dégâts")

        if not cible.est_vivant():
            messages.append(f"{cible.nom} est K.O.!")

        # Gérer les buffs de tous les héros
        for hero in self.equipe:
            hero.gerer_buffs()

        return {"messages": messages, "degats_total": degats_total}

    def tour_de_combat_complet(self, monstre):
        """
        Gère un tour de combat complet (tous les héros + monstre)
        Version simplifiée pour le mode auto
        """
        resultat = {
            "monstre_vivant": monstre.est_vivant(),
            "heros_vivants": [h.est_vivant() for h in self.equipe],
            "degats_joueur": 0,
            "degats_monstre": 0,
            "tour": self.tour,
            "messages": []
        }

        self.tour += 1
        self.tours_cumule += 1
        
        # Tour des héros
        tour_heros = self.tour_heros_complet(monstre)
        resultat["degats_joueur"] = tour_heros["degats_totaux"]
        resultat["messages"].extend(tour_heros["messages"])

        # Tour du monstre (si toujours vivant)
        if monstre.est_vivant():
            tour_monstre = self.tour_monstre(monstre)
            resultat["degats_monstre"] = tour_monstre["degats_total"]
            resultat["messages"].extend(tour_monstre["messages"])
        
        # Mettre à jour les états
        resultat["monstre_vivant"] = monstre.est_vivant()
        resultat["heros_vivants"] = [h.est_vivant() for h in self.equipe]

        return resultat
    
    def verifier_defaite(self):
        """Vérifie si tous les héros sont K.O."""
        return all(not h.est_vivant() for h in self.equipe)
    
    def verifier_victoire(self):
        """Vérifie si tous les monstres ont été vaincus"""
        return self.monstre_actuel_index >= len(self.monstres)
    
    def initialiser_combat(self):
        """Initialise un nouveau combat"""
        self.charger_items()
        self.charger_monstres()
        self.victoires = 0
        self.monstre_actuel_index = 0
        # Compteur de tours par combat et cumul global
        self.tour = 1
        self.tours_cumule = 0
        self.hero_actuel_index = 0
        
        # Donner un item de départ si demandé (nom fixé), sinon générer un item aléatoire
        try:
            if self.equipe:
                hero = self.equipe[0]
                if self.start_item_name:
                    # Utiliser le nom fourni
                    item = test_item_giver(self.equipe, self.start_item_name, trigger_event=self.start_item_trigger_event)
                    if item:
                        print(f"Item de départ (fixe): {item.nom} équipé sur {hero.nom}")
                else:
                    from items import obtenir_item, equiper_item_a_hero
                    item = obtenir_item(self.equipe, {'commun': 40, 'peu_commun': 30, 'rare': 20, 'legendaire': 10}, self.items_par_rarete)
                    if item:
                        equiper_item_a_hero(hero, item)
                        verifier_effet_items(self.equipe)
                        events.trigger("obtention_item", hero, item, self.equipe)
                        print(f"Item de départ (aléatoire): {item.nom} équipé sur {hero.nom}")
        except Exception as e:
            print(f"[Start Item] Erreur lors de l'attribution: {e}")
    
    def sauvegarder_score(self, victoires):
        """Sauvegarde le score dans la base de données ET en JSON local"""
        nom_joueur = self.nom_joueur if self.nom_joueur and self.nom_joueur.strip() else "Joueur"
        
        score_data = {
            "nom_joueur": nom_joueur,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "equipe": [h.nom for h in self.equipe],
            "victoires": victoires,
            "total_monstres": len(self.monstres),
            "tours": self.tours_cumule
        }
        
        # Sauvegarder en MongoDB
        db.scores.insert_one({
            "nom_joueur": nom_joueur,
            "date": datetime.now(),
            "equipe": [h.nom for h in self.equipe],
            "victoires": victoires,
            "total_monstres": len(self.monstres),
            "tours": self.tours_cumule
        })
        
        # Sauvegarder en JSON local (10 derniers scores)
        self.sauvegarder_scores_json(score_data)
        
    def sauvegarder_scores_json(self, nouveau_score):
        """Sauvegarde les 10 derniers scores dans un fichier JSON local"""
        import json
        import os
        
        fichier_scores = "scores.json"
        scores = []
        
        # Charger les scores existants
        if os.path.exists(fichier_scores):
            try:
                with open(fichier_scores, 'r', encoding='utf-8') as f:
                    scores = json.load(f)
            except:
                scores = []
        
        # Ajouter le nouveau score en début
        scores.insert(0, nouveau_score)
        
        # Garder seulement les 10 derniers
        scores = scores[:10]
        
        # Sauvegarder en JSON
        try:
            with open(fichier_scores, 'w', encoding='utf-8') as f:
                json.dump(scores, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde JSON: {e}")
        
    def reinitialiser_equipe(self):
        """Réinitialise la vie de l'équipe (entre les monstres)"""
        for hero in self.equipe:
            if hasattr(hero, 'pv_max'):
                hero.pv = hero.pv_max
            # Reset d'autres états si nécessaire
            hero.peut_attaquer = True
            if hasattr(hero, 'cooldowns'):
                hero.cooldowns = {}