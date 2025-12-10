import pygame
from attaques import obtenir_attaques_disponibles, gerer_cooldown_attaque

class Combat:
    def __init__(self, game):
        self.game = game
        self.font_title = pygame.font.Font(None, 50)
        self.font_text = pygame.font.Font(None, 30)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 20)
        
        # État du combat
        self.hero_actuel_index = 0
        self.en_attente_action = True
        self.messages = []
        self.message_timer = 0
        
        # Boutons d'attaque
        self.boutons_attaques = []
        self.creer_boutons_attaques()

        # Mémo pour les métamorphoses (savoir quelle attaque a été choisie)
        self.pending_metamorphose = None
        
        # Bouton passer le tour (aligné à droite des attaques, plus compact en hauteur)
        self.btn_passer = pygame.Rect(880, 540, 200, 70)
        
    def creer_boutons_attaques(self):
        """Crée les boutons pour les attaques du héros actuel"""
        self.boutons_attaques = []
        
        # Vérifier si le héros courant est vivant, sinon passer au suivant
        while self.hero_actuel_index < len(self.game.equipe):
            hero = self.game.equipe[self.hero_actuel_index]
            if hero.est_vivant():
                break
            self.hero_actuel_index += 1
        
        # Si tous les héros sont morts ou index invalide, lancer le tour du monstre
        if self.hero_actuel_index >= len(self.game.equipe):
            self.tour_monstre()
            return
        
        hero = self.game.equipe[self.hero_actuel_index]
        attaques = obtenir_attaques_disponibles(hero)
        
        y_start = 520
        for idx, (type_attaque, attaque_info) in enumerate(attaques):
            btn = {
                "rect": pygame.Rect(40 + idx * 280, y_start, 250, 110),
                "type": type_attaque,
                "info": attaque_info,
                "cooldown": hero.cooldowns.get(type_attaque, 0)
            }
            self.boutons_attaques.append(btn)
    
    def passer_au_hero_suivant(self):
        """Passe au héros suivant qui peut agir"""
        self.hero_actuel_index += 1
        
        # Chercher le prochain héros vivant
        while self.hero_actuel_index < len(self.game.equipe):
            if self.game.equipe[self.hero_actuel_index].est_vivant():
                break
            self.hero_actuel_index += 1
        
        # Si tous les héros ont joué
        if self.hero_actuel_index >= len(self.game.equipe):
            self.tour_monstre()
        else:
            self.creer_boutons_attaques()
    
    def tour_monstre(self):
        """Exécute le tour du monstre"""
        monstre = self.game.obtenir_monstre_actuel()
        if not monstre:
            return
        
        resultat = self.game.tour_monstre(monstre)
        self.messages = resultat["messages"]
        self.message_timer = 180  # 3 secondes à 60 FPS
        
        # Vérifier la défaite
        if self.game.verifier_defaite():
            from screens.defaite import Defaite
            self.game.change_screen(Defaite)
            return
        
        # Réduire les cooldowns et préparer le prochain tour
        for hero in self.game.equipe:
            hero.reduire_cooldowns()
        
        self.hero_actuel_index = 0
        self.en_attente_action = True
        self.creer_boutons_attaques()
    
    def update(self):
        # Décompter le timer des messages
        if self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer == 0:
                self.messages = []
    
    def handle_events(self, event_list):
        if not self.en_attente_action:
            return
        
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Vérifier les boutons d'attaque
                for btn in self.boutons_attaques:
                    if btn["rect"].collidepoint(event.pos) and btn["cooldown"] == 0:
                        resultat = self.executer_attaque(self.hero_actuel_index, btn["type"], btn["info"])
                        
                        # Vérifier si c'est une métamorphose qui demande une sélection
                        if resultat.get("selection_forme"):
                            # Mémoriser l'attaque pour gérer le cooldown/fin de tour après choix
                            self.pending_metamorphose = {"type": btn["type"], "info": btn["info"]}
                            self.ouvrir_selection_forme(resultat)
                            return
                        
                        self.traiter_resultat_attaque(resultat)
                        break
                
                # Bouton passer
                if self.btn_passer.collidepoint(event.pos):
                    self.passer_au_hero_suivant()
    
    def ouvrir_selection_forme(self, resultat):
        """Ouvre l'écran de sélection de forme pour la druidesse"""
        hero = self.game.equipe[self.hero_actuel_index]
        monstre = self.game.obtenir_monstre_actuel()
        formes = resultat.get("formes_disponibles", [])
        
        # Afficher les messages avant la sélection
        self.messages = resultat.get("messages", [])
        self.message_timer = 120
        
        # Créer l'écran de sélection avec callback
        from screens.selection_forme import SelectionForme
        
        def callback_retour(msg_transfo):
            # Appliquer le cooldown de l'attaque de métamorphose (si connu)
            if self.pending_metamorphose:
                hero = self.game.equipe[self.hero_actuel_index]
                gerer_cooldown_attaque(hero, self.pending_metamorphose["type"], self.pending_metamorphose["info"])
                self.pending_metamorphose = None

            # Ajouter le message de transformation et passer au héros suivant immédiatement
            self.messages = [msg_transfo]
            self.message_timer = 120
            self.game.change_screen(Combat)
            self.passer_au_hero_suivant()
        
        selection_forme = SelectionForme(
            self.game, 
            hero, 
            monstre, 
            self.game.equipe, 
            formes, 
            callback_retour
        )
        self.game.change_screen(lambda game: selection_forme)
    
    def executer_attaque(self, hero_index, type_attaque, attaque_info):
        """Exécute l'attaque du héros spécifié par index"""
        hero = self.game.equipe[hero_index]
        monstre = self.game.obtenir_monstre_actuel()
        
        resultat = self.game.tour_hero_unique(hero, monstre, type_attaque, attaque_info)
        
        # IMPORTANT : Retourner le résultat au lieu de le traiter directement
        return resultat

    def traiter_resultat_attaque(self, resultat):
        """Traite le résultat d'une attaque normale"""
        self.messages = resultat.get("messages", [])
        self.message_timer = 120  # 2 secondes

        # Si un item est créé en plein combat (ex: singe savant), ouvrir la sélection d'item
        if resultat.get("ouvrir_selection_item") and resultat.get("item_cree"):
            from screens.selection_item import SelectionItem
            self.game.change_screen(lambda g: SelectionItem(g, item_override=resultat["item_cree"], retour_combat=True))
            return
        
        # Vérifier si le monstre est mort
        if not resultat.get("monstre_vivant", True):
            self.game.victoires += 1
            # Passer à l'écran de sélection d'item
            from screens.selection_item import SelectionItem
            self.game.change_screen(SelectionItem)
            return
        
        # Passer au héros suivant
        self.passer_au_hero_suivant()
    
    def draw(self, screen):
        # Titre
        title = self.font_title.render(f"Combat - Tour {self.game.tour}", True, (255, 255, 255))
        screen.blit(title, (self.game.WIDTH // 2 - title.get_width() // 2, 20))
        
        # Afficher l'équipe (en haut à gauche)
        self.afficher_equipe(screen)
        
        # Afficher le monstre (au centre)
        self.afficher_monstre(screen)
        
        # Afficher le héros actuel
        if self.hero_actuel_index < len(self.game.equipe):
            hero = self.game.equipe[self.hero_actuel_index]
            # si le hero a des stacks, les afficher
            
            if hero.est_vivant():
                hero_text = self.font_text.render(f"C'est au tour de : {hero.nom}", True, (255, 255, 100))
                screen.blit(hero_text, (50, 480))
            if hasattr(hero, 'stack') and hero.stack > 0:
                stack_text = self.font_small.render(f"Stacks: {hero.stack}", True, (255, 255, 100))
                screen.blit(stack_text, (50, 520))
        
        # Dessiner les boutons d'attaque avec description
        mouse_pos = pygame.mouse.get_pos()

        def wrap(text, font, max_width):
            words = text.split()
            lines = []
            cur = ""
            for w in words:
                tentative = f"{cur} {w}".strip()
                if font.size(tentative)[0] <= max_width:
                    cur = tentative
                else:
                    if cur:
                        lines.append(cur)
                    cur = w
            if cur:
                lines.append(cur)
            return lines

        for btn in self.boutons_attaques:
            # Couleur selon disponibilité
            if btn["cooldown"] > 0:
                color = (80, 80, 80)
            elif btn["rect"].collidepoint(mouse_pos):
                color = (100, 100, 200)
            else:
                color = (70, 70, 150)
            
            pygame.draw.rect(screen, color, btn["rect"])
            pygame.draw.rect(screen, (200, 200, 200), btn["rect"], 2)
            
            # Nom de l'attaque
            nom = self.font_text.render(btn["info"].get("nom", "Attaque"), True, (255, 255, 255))
            screen.blit(nom, (btn["rect"].x + 12, btn["rect"].y + 10))
            
            # Description
            desc = btn["info"].get("description", "")
            if desc:
                lines = wrap(desc, self.font_tiny, btn["rect"].width - 24)
                for i, line in enumerate(lines[:3]):
                    txt = self.font_tiny.render(line, True, (220, 220, 240))
                    screen.blit(txt, (btn["rect"].x + 12, btn["rect"].y + 38 + i * 16))

            # Cooldown ou info
            if btn["cooldown"] > 0:
                cd_text = self.font_small.render(f"attente: {btn['cooldown']}", True, (255, 100, 100))
                screen.blit(cd_text, (btn["rect"].x + 12, btn["rect"].y + 90))
            else:
                dmg_text = self.font_small.render("Prêt", True, (200, 200, 200))
                screen.blit(dmg_text, (btn["rect"].x + 12, btn["rect"].y + 90))
        
        # Bouton passer le tour
        passer_color = (120, 80, 80) if self.btn_passer.collidepoint(mouse_pos) else (90, 60, 60)
        pygame.draw.rect(screen, passer_color, self.btn_passer)
        pygame.draw.rect(screen, (200, 150, 150), self.btn_passer, 2)
        passer_txt = self.font_text.render("Passer", True, (255, 230, 230))
        screen.blit(passer_txt, (self.btn_passer.centerx - passer_txt.get_width() // 2, self.btn_passer.centery - passer_txt.get_height() // 2))

       
        # Afficher les messages
        self.afficher_messages(screen)
    
    def afficher_equipe(self, screen):
        """Affiche l'équipe en haut à gauche avec stats, statuts, buffs et items"""
        x = 30
        y = 80
        
        title = self.font_text.render("Votre équipe :", True, (150, 255, 150))
        screen.blit(title, (x, y))
        y += 40
        
        for idx, hero in enumerate(self.game.equipe):
            # Couleur selon l'état
            if not hero.est_vivant():
                color = (100, 100, 100)
            elif idx == self.hero_actuel_index:
                color = (255, 255, 100)
            else:
                color = (200, 200, 200)
            
            # Nom
            nom_text = self.font_small.render(f"{hero.nom}", True, color)
            screen.blit(nom_text, (x, y))
            y += 22
            
            # Stats (ATK / DEF)
            stats_text = self.font_small.render(f"ATK: {hero.atk} | DEF: {hero.defense}", True, (180, 180, 180))
            screen.blit(stats_text, (x, y))
            y += 22
            
            # Barre de vie
            hp_percent = hero.pv / hero.pv_max if hero.pv_max > 0 else 0
            barre_width = 200
            barre_height = 15
            
            # Fond de la barre
            pygame.draw.rect(screen, (50, 50, 50), (x, y, barre_width, barre_height))
            # Barre de vie
            pygame.draw.rect(screen, (100, 200, 100), (x, y, int(barre_width * hp_percent), barre_height))
            # Contour
            pygame.draw.rect(screen, (200, 200, 200), (x, y, barre_width, barre_height), 1)
            
            # HP text
            hp_text = self.font_small.render(f"{hero.pv}/{hero.pv_max}", True, (255, 255, 255))
            screen.blit(hp_text, (x + barre_width + 10, y))
            y += 20
            
            # Statuts (poison, stun, brûlure, etc.)
            statuts_affichage = []
            if hasattr(hero, 'status') and hero.status:
                for statut in hero.status:
                    stat_type = statut.get('stat', '')
                    tours_restants = statut.get('tours_restants', 0)
                    
                    if tours_restants > 0:
                        # Créer des noms courts pour chaque statut
                        nom_court = {
                            'poison': 'Poison',
                            'stun': 'Stun',
                            'brulure': 'Brûlure',
                            'saignement': 'Saigne',
                            'regen': 'Regen',
                            'prendre_focus': 'Focus',
                        }.get(stat_type, stat_type.capitalize())
                        
                        statuts_affichage.append(f"{nom_court}({tours_restants}t)")
            
            if statuts_affichage:
                statuts_text = " | ".join(statuts_affichage)
                status_surface = self.font_small.render(statuts_text, True, (255, 150, 150))
                screen.blit(status_surface, (x, y))
                y += 22
            
            # Buffs (bonus temporaires)
            buffs_affichage = []
            if hasattr(hero, 'buffs') and hero.buffs:
                for buff in hero.buffs:
                    buff_stat = buff.get('stat', '')
                    montant = buff.get('montant', 0)
                    tours_restants = buff.get('tours_restants', 0)
                    
                    if tours_restants > 0:
                        if buff_stat == 'atk':
                            buffs_affichage.append(f"+{montant}ATK({tours_restants}t)")
                        elif buff_stat == 'defense':
                            buffs_affichage.append(f"+{montant}DEF({tours_restants}t)")
                        elif buff_stat == 'pv_max':
                            buffs_affichage.append(f"+{montant}HP({tours_restants}t)")
                        else:
                            buffs_affichage.append(f"+{montant}{buff_stat.upper()}({tours_restants}t)")
            
            if buffs_affichage:
                buffs_text = " | ".join(buffs_affichage)
                buffs_surface = self.font_small.render(buffs_text, True, (150, 200, 255))
                screen.blit(buffs_surface, (x, y))
                y += 22
            
            # Items équipés
            items = []
            if hasattr(hero, 'items') and hero.items:
                for item in hero.items:
                    # Vérifier si c'est un objet ou un dictionnaire
                    if hasattr(item, 'nom'):
                        nom_item = item.nom
                    elif isinstance(item, dict):
                        nom_item = item.get('nom', 'Item')
                    else:
                        nom_item = str(item)
                    
                    # Limiter à 15 caractères pour l'affichage
                    if len(nom_item) > 15:
                        nom_item = nom_item[:12] + "..."
                    items.append(nom_item)
            
            if items:
                # Afficher maximum 2 items par ligne
                for i in range(0, len(items), 2):
                    items_ligne = " | ".join(items[i:i+2])
                    items_surface = self.font_small.render(items_ligne, True, (255, 200, 100))
                    screen.blit(items_surface, (x, y))
                    y += 22
            
            # Espacement entre les héros
            y += 10
            
            # Ligne de séparation
            if idx < len(self.game.equipe) - 1:
                pygame.draw.line(screen, (100, 100, 100), (x, y), (x + 300, y), 1)
                y += 10
    
    def afficher_monstre(self, screen):
        """Affiche le monstre au centre"""
        monstre = self.game.obtenir_monstre_actuel()
        if not monstre:
            return
        
        x = self.game.WIDTH // 2 - 150
        y = 150
        
        # Nom
        nom = self.font_title.render(monstre.nom, True, (255, 100, 100))
        screen.blit(nom, (x, y))
        
        # Barre de vie
        hp_percent = monstre.pv / monstre.pv_max if monstre.pv_max > 0 else 0
        barre_width = 300
        barre_height = 25
        
        pygame.draw.rect(screen, (50, 50, 50), (x, y + 60, barre_width, barre_height))
        pygame.draw.rect(screen, (200, 50, 50), (x, y + 60, int(barre_width * hp_percent), barre_height))
        pygame.draw.rect(screen, (200, 200, 200), (x, y + 60, barre_width, barre_height), 2)
        
        # HP text
        hp_text = self.font_text.render(f"{monstre.pv}/{monstre.pv_max}", True, (255, 255, 255))
        screen.blit(hp_text, (x + barre_width + 10, y + 60))
        
        # Stats
        stats_text = self.font_small.render(f"ATK: {monstre.atk} | DEF: {monstre.defense}", True, (200, 200, 200))
        screen.blit(stats_text, (x, y + 100))
        
        y += 130
        
        # Statuts du monstre
        statuts_affichage = []
        if hasattr(monstre, 'status') and monstre.status:
            for statut in monstre.status:
                stat_type = statut.get('stat', '')
                tours_restants = statut.get('tours_restants', 0)
                
                if tours_restants > 0:
                    nom_court = {
                        'poison': 'Poison',
                        'stun': 'Stun',
                        'brulure': 'Brûlure',
                        'saignement': 'Saigne',
                        'regen': 'Regen',
                        'prendre_focus': 'Focus',
                    }.get(stat_type, stat_type.capitalize())
                    
                    statuts_affichage.append(f"{nom_court}({tours_restants}t)")
        
        if statuts_affichage:
            statuts_text = " | ".join(statuts_affichage)
            status_surface = self.font_small.render(statuts_text, True, (255, 150, 150))
            screen.blit(status_surface, (x, y))
            y += 22
    
    def afficher_messages(self, screen):
        """Affiche les messages de combat"""
        if not self.messages:
            return
        
        x = self.game.WIDTH // 2 - 300
        y = 350
        
        # Fond semi-transparent
        surface = pygame.Surface((600, 100))
        surface.set_alpha(200)
        surface.fill((30, 30, 30))
        screen.blit(surface, (x, y))
        
        # Bordure
        pygame.draw.rect(screen, (200, 200, 200), (x, y, 600, 100), 2)
        
        # Messages
        y += 10
        for msg in self.messages[-3:]:  # Afficher seulement les 3 derniers messages
            text = self.font_small.render(msg, True, (255, 255, 255))
            screen.blit(text, (x + 10, y))
            y += 28