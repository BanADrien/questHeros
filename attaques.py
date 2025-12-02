# === attaques.py ===

from multiprocessing import reduction


def executer_attaque(attaquant, cible, type_attaque, attaque_info):
    # Récupérer la fonction Python
    nom_fonction = attaque_info["fonction"]
    
    if not hasattr(__import__(__name__), nom_fonction):
        raise ValueError(f"La fonction d’attaque '{nom_fonction}' n’existe pas dans attaques.py")

    fonction_attaque = getattr(__import__(__name__), nom_fonction)

    print(f"\n{attaquant.nom} utilise {attaque_info['nom']} ! (Type : {type_attaque})")

    # Exécuter la fonction d’attaque
    degats_total = fonction_attaque(attaquant, cible)

    # Afficher le résultat
    print(f"> {degats_total} dégâts infligés à {cible.nom} !")

    if not cible.est_vivant():
        print(f"{cible.nom} est mort !")

    return degats_total

# logique fais avec chatgpt 
def calcule_reduction_defense(cible, degats):
    reduction = cible.defense / (cible.defense + 100)
    degats_reels = max(1, int(degats * (1 - reduction)))
    return degats_reels
    
# liste des attaques disponibles

# Archer 

def tir_rapide(attaquant, cible):
    degats = int(attaquant.atk * 0.75)
    return cible.prendre_degats(degats)


def double_tir(attaquant, cible):
    total = 0
    for i in range(2):
        deg = int(attaquant.atk * 0.40)
        total += cible.prendre_degats(deg)
        print(f"- Coup {i+1} : {deg} bruts → {deg} après défense")
    return total


def pluie_de_fleches(attaquant, cible):
    from random import randint
    total = 0
    
    for i in range(10):
        pourcentage = randint(20, 100)
        deg = int(attaquant.atk * (pourcentage / 100))
        total += cible.prendre_degats(deg)
        print(f"- Flèche {i+1} : {pourcentage}% → {deg} dégâts")
    
    return total

# mage

def arcane_simple(attaquant, cible):
    degats = int(attaquant.atk * 0.30)
    degats_infliges = cible.prendre_degats(degats)
    reduction_defense = int(attaquant.atk * 0.1)
    cible.defense = max(0, cible.defense - reduction_defense)
    print(f"> La défense de {cible.nom} est réduite de {reduction_defense} points.")
    return degats_infliges





def obtenir_attaques_disponibles(hero):
    attaques_dispo = []

    # Attaque de base 
    attaques_dispo.append(("base", hero.attaques["base"]))

    # Spéciale
    if hero.cooldowns["special"] == 0:
        attaques_dispo.append(("special", hero.attaques["special"]))

    # Ultime
    if hero.cooldowns["ultime"] == 0:
        attaques_dispo.append(("ultime", hero.attaques["ultime"]))

    return attaques_dispo



def gerer_cooldown_attaque(hero, type_attaque, attaque_info):
    if type_attaque == "special" or type_attaque == "ultime":
        hero.cooldowns[type_attaque] = attaque_info["cooldown"]

