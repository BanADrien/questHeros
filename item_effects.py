import effects

# STATUS


def item_brulure(joueur, event):
    
    cible = event["cible"]
    tours = event["tours"]

    effects.brulure(cible, tours)
    return f"{joueur.nom} inflige Brûlure à {cible.nom} !"


def item_saignement(joueur, event):
    cible = event["cible"]
    degats_total = event["degats_total"]
    attaque_type = event.get("attaque_type", None)
    tours = event["tours"]

    effects.saignement(cible, degats_total, tours)
    return f"{joueur.nom} inflige Saignement à {cible.nom} !"

def item_poison(joueur, event):
    cible = event["cible"]
    tours = event["tours"]

    effects.poison(cible, tours)
    return f"{joueur.nom} empoisonne {cible.nom} !"

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
    return f"{joueur.nom} se régénère de {montant} PV !"


# SPECIAUX


def item_prendre_focus(joueur, event):
    """Le joueur qui a cet item attire les attaques du monstre"""
    joueur.est_cible = True
    return f"{joueur.nom} attire l'attention des ennemis !"


def item_transformation_hero(joueur, event):
    attaquant = event["attaquant"]
    equipe = event["equipe"]
    
    # Transformation immédiate lors de l'obtention du Cape du héro
    # Ne pas transformer si déjà Héro ou Légende
    if attaquant.nom not in ["Héro", "Légende"]:
        degats, msg = effects.transformation(attaquant, "Héro", equipe)
        return msg
    return f"{attaquant.nom} est déjà un héros légendaire !"
