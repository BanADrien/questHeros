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

    effects.effet_vol_de_vie(degats_total, attaquant)


# SOIN


def item_regen(joueur, event):
    attaquant = event["attaquant"]
    montant = event["montant"]
    tours = event["tours"]

    effects.effet_regen(attaquant, montant, tours)


# SPECIAUX


def item_prendre_focus(joueur, event):
    """Le joueur qui a cet item attire les attaques du monstre"""
    print(f"> {joueur.nom} attire l'attention des ennemis jusqu'à la fin de la partie !")
    joueur.est_cible = True


def item_transformation_hero(joueur, event):
    attaquant = event["attaquant"]
    equipe = event["equipe"]
    
    # Transformation immédiate lors de l'obtention du Cape du héro
    # Ne pas transformer si déjà Héro ou Légende
    if attaquant.nom not in ["Héro", "Légende"]:
        effects.transformation(attaquant, "Héro", equipe)
