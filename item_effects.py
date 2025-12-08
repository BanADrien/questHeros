import effects 
# status

def item_brulure(attaquant, cible, equipe, montant, tours, attaque_type):
    if attaque_type == "special":
        effects.brulure(cible, tours)
    
def item_saignement(attaquant, cible, equipe, montant, tours, attaque_type):
    effects.saignement(cible, montant, tours)
    
def item_vol_de_vie(attaquant, cible, equipe, montant, tours, attaque_type):
    if attaque_type == "base" :
        effects.effet_vol_de_vie(montant, attaquant)
    
# soin

def item_regen(attaquant, cible, equipe, montant, tours, attaque_type):
    effects.effet_regen(cible=attaquant, montant=montant, tours=tours, print=False)
    
    
# speciaux
    
def item_prendre_focus(attaquant, cible, equipe, montant, tours, attaque_type):
    print(f"> {cible.nom} attire l'attention des ennemis jusqu'a la fin de la partie !")
    attaquant.est_cible = True
    
def item_transformation_hero(attaquant, cible, equipe, montant, tours, attaque_type):
    
    if attaquant.nom != "Héro" and attaquant.nom != "Légende" and attaque_type == "ultime":
        effects.transformation(attaquant, "Héro", equipe)