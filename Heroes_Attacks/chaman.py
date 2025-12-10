from effects import buff_stat, effet_regen, brulure, poison
import random

def totem_regen(attaquant, cible, equipe):
    messages = []
    for membre in equipe:
        _, msg_part = effet_regen(membre, 5, 1)
        messages.append(msg_part)
    
    return {"degats": 0, "messages": messages}


def totem_brulure(attaquant, cible, equipe):
    _, msg = brulure(cible, 3)
    return {"degats": 0, "messages": [msg]}


def totem_poison(attaquant, cible, equipe):
    _, msg = poison(cible, 3)
    return {"degats": 0, "messages": [msg]}


def totem_degats(attaquant, cible, equipe):
    degats = int(attaquant.atk * 1.00)
    reels = cible.prendre_degats(degats)
    return {"degats": reels, "messages": [f"Le totem inflige {reels} dégâts à {cible.nom} !"]}


def totem(attaquant, cible, equipe):
    totems = [
        ("Régénération", totem_regen),
        ("Brûlure", totem_brulure),
        ("Poison", totem_poison),
        ("Dégâts", totem_degats)
    ]
    nom_totem, totem_choisi = random.choice(totems)
    resultat = totem_choisi(attaquant, cible, equipe)
    
    # Ajouter le message du totem invoqué au début
    resultat["messages"].insert(0, f"Le totem invoqué est : {nom_totem}")
    
    return resultat


def totem_de_guerre(attaquant, cible, equipe):
    messages = []
    for membre in equipe:
        montant_boost_atk = int(membre.atk * 0.30)
        _, msg = buff_stat(membre, "atk", montant_boost_atk, 2)
        messages.append(msg)
    
    return {"degats": 0, "messages": messages}


def totem_de_survie(attaquant, cible, equipe):
    montant_boost_def = 10
    montant_regen = 10
    messages = []
    
    for membre in equipe:
        _, msg_def = buff_stat(membre, "defense", montant_boost_def, 3)
        messages.append(msg_def)
        
        _, msg_regen = effet_regen(membre, montant_regen, 3)
        messages.append(msg_regen)
    
    return {"degats": 0, "messages": messages}