import effects

# STATUS


def item_brulure(joueur, event):
    
    cible = event["cible"]
    tours = event["tours"]


    effects.brulure(cible, tours)


def item_saignement(joueur, event):
    cible = event["cible"]
    degats_total = event["degats_total"]
    attaque_type = event.get("attaque_type", None)
    if attaque_type == "base":
        tours = event["tours"]

    effects.saignement(cible, degats_total, tours)

def item_poison(joueur, event):
    cible = event["cible"]
    tours = event["tours"]

    effects.poison(cible, tours)

def item_vol_de_vie(joueur, event):
    attaquant = event["attaquant"]
    attaque_type = event.get("attaque_type", None)
    degats_total = event["degats_total"]

    if attaque_type == "base":
        effects.effet_vol_de_vie(degats_total, attaquant)


# SOIN


def item_regen(joueur, event):
    attaquant = event["attaquant"]
    montant = event["montant"]
    tours = event["tours"]

    effects.effet_regen(cible=attaquant, montant=montant, tours=tours, print=False)


# SPECIAUX


def item_prendre_focus(joueur, event):
    attaquant = event["attaquant"]
    cible = event["cible"]

    print(f"> {cible.nom} attire l'attention des ennemis jusqu'à la fin de la partie !")
    attaquant.est_cible = True


def item_transformation_hero(joueur, event):
    attaquant = event["attaquant"]
    equipe = event["equipe"]
    attaque_type = event.get("attaque_type", None)

    if attaquant.nom not in ["Héro", "Légende"] and attaque_type == "ultime":
        effects.transformation(attaquant, "Héro", equipe)
