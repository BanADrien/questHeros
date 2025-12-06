from attaques import obtenir_attaques_disponibles, executer_attaque, gerer_cooldown_attaque
from utils import afficher_details_attaque, afficher_monstre

def tour_hero(self, hero, monstre):
    print(f"\nC'est au tour de {hero.nom}!")
        
    hero.appliquer_status()
    if hero.peut_attaquer == False:
        return
    else:
        afficher_details_attaque(hero)
        attaques_dispo = obtenir_attaques_disponibles(hero)
        
        choix = self.choisir_attaque(hero)
        type_attaque, attaque_info = attaques_dispo[choix - 1]

        
        executer_attaque(hero, monstre, self.equipe, type_attaque, attaque_info)
        afficher_monstre(monstre)
    
    gerer_cooldown_attaque(hero, type_attaque, attaque_info)