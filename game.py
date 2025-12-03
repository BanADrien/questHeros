import random
import os
from datetime import datetime
from models import Combattant
from items import obtenir_loot_apres_combat
from db_init import get_db
from utils import (
    menu_principale_de_combat, afficher_etat_combat, afficher_details_attaque, 
    afficher_intro_combat, afficher_tour, afficher_resultat_combat,
    afficher_equipe, afficher_monstre
)
from attaques import (
    executer_attaque, obtenir_attaques_disponibles, 
    gerer_cooldown_attaque
)

db = get_db()

class Partie:
    def __init__(self):
        self.equipe = []
        self.monstres = []
        self.items = []
        self.monstre_actuel_index = 0
        self.tour = 0
    
    def choisir_equipe(self):
        personnages_dispo = list(db.personnages.find())
        print("\n" + "="*50)
        print("SÉLECTION DE L'ÉQUIPE")
        print("="*50)
        
        for i in range(3):
            print(f"\nChoix du héros {i+1}/3:")
            print("-" * 40)
            for id, perso in enumerate(personnages_dispo, start=1):
                print(f"{id}. {perso['nom']} - ATK:{perso['atk']} DEF:{perso['def']} PV:{perso['pv_max']}")
            
            while True:
                try:
                    choix = int(input(f"\nChoisissez le héros {i+1}: "))
                    if 1 <= choix <= len(personnages_dispo):
                        perso_choisi = personnages_dispo.pop(choix - 1)
                        self.equipe.append(Combattant(perso_choisi, est_heros=True))
                        print(f"{perso_choisi['nom']} rejoint l'équipe!")
                        break
                except ValueError:
                    print("mets un nombre valide")
        
        print("\nVotre équipe est prête!")
        for hero in self.equipe:
            print(f"  - {hero.nom}")
    
    def charger_monstres(self):
        monstres_data = list(db.monstres.find())
        for monstre_data in monstres_data:
            self.monstres.append(Combattant(monstre_data, est_heros=False))
    def charger_items(self):
        items_data = list(db.items.find())
        self.items = items_data
        
    def tour_heros(self, monstre):
        for hero in self.equipe:
            if not hero.est_vivant():
                continue
            
            if not monstre.est_vivant():
                break
            
            afficher_etat_combat(monstre, self.equipe)
            print(f"\nC'est au tour de {hero.nom}!")
            
           
            afficher_details_attaque(hero)
            attaques_dispo = obtenir_attaques_disponibles(hero)
            
            choix = self.choisir_attaque(hero)
            type_attaque, attaque_info = attaques_dispo[choix - 1]

            
            executer_attaque(hero, monstre, self.equipe, type_attaque, attaque_info)
            afficher_monstre(monstre)
          
            gerer_cooldown_attaque(hero, type_attaque, attaque_info)
        
        
        for hero in self.equipe:
            hero.reduire_cooldowns()
    
    def choisir_attaque(self, hero):
        while True:
            try:
                choix = int(input("\nChoisissez une attaque (1-3): "))

                if choix not in (1, 2, 3):
                    print(" Cette attaque n'existe pas.")
                    continue

                type_attaque = ["base", "special", "ultime"][choix - 1]

                # Vérification du cooldown
                if hero.cooldowns.get(type_attaque, 0) > 0:
                    print(f" L'attaque {type_attaque} est en cooldown ({hero.cooldowns[type_attaque]} tours).")
                    continue

                return choix

            except ValueError:
                print("Entrée invalide !")

    
    def tour_monstre(self, monstre):
        if not monstre.est_vivant():
            return
        
        cibles_vivantes = [h for h in self.equipe if h.est_vivant()]
        if not cibles_vivantes:
            return
        
        cible = random.choice(cibles_vivantes)
        print(f"\n{monstre.nom} attaque {cible.nom}!")
        
        degats = monstre.atk
        degats_reels = cible.prendre_degats(degats)
        print(f"{degats_reels} dégâts infligés à {cible.nom}!")
        attente = input("Appuyez sur Entrée pour continuer...")
        
        
        if not cible.est_vivant():
            print(f"{cible.nom} est K.O.!")
        
        afficher_equipe(self.equipe)
        for hero in self.equipe:
            hero.gerer_buffs()

        


    
    def combattre_monstre(self, monstre):

        afficher_intro_combat(monstre)

        while monstre.est_vivant() and any(h.est_vivant() for h in self.equipe):
            self.tour += 1
            afficher_tour(self.tour)
            menu_principale_de_combat()

            choix = input("\nVotre choix: ")

            if choix == "1":
                
                self.tour_heros(monstre)
                
                if monstre.est_vivant():
                    monstre.appliquer_status()
                    self.tour_monstre(monstre)
                    

            elif choix == "2":
               
                os.system('cls' if os.name == 'nt' else 'clear')
                afficher_equipe(self.equipe)
                
                continue  

            else:
                print("Choix invalide, recommence.")
                continue


        return not monstre.est_vivant()

    
    def lancer(self):
        print("\n" + "="*60)
        print("BIENVENUE DANS MON JEU SUPERRRRRR")
        print("="*60)
        
        self.choisir_equipe()
        self.charger_items()
        self.charger_monstres()
        
        print(f"\nVous allez affronter {len(self.monstres)} monstres!")
        input("\nAppuyez sur Entrée pour commencer l'aventure...")
        
        victoires = 0
        for monstre in self.monstres:
            victoire = self.combattre_monstre(monstre)
            
            if victoire:
                victoires += 1
                afficher_resultat_combat(True, monstre, victoires, len(self.monstres))
                
                obtenir_loot_apres_combat(self.equipe, self.items)
                
                if monstre != self.monstres[-1]:
                    input("\nAppuyez sur Entrée pour affronter le prochain monstre...")
            else:
                afficher_resultat_combat(False, monstre, victoires, len(self.monstres))
                break
        
        if victoires == len(self.monstres):
            print("\n" + "="*60)
            print("FÉLICITATIONS! VOUS AVEZ VAINCU TOUS LES MONSTRES!")
            print("="*60)
        
        # Sauvegarder le score
        self.sauvegarder_score(victoires)
    
    def sauvegarder_score(self, victoires):
        db.scores.insert_one({
            "date": datetime.now(),
            "equipe": [h.nom for h in self.equipe],
            "victoires": victoires,
            "total_monstres": len(self.monstres),
            "tours": self.tour
        })
