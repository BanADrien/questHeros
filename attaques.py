# === attaques.py ===

import random


# ----------------------------------------------------
#  FONCTION PRINCIPALE D’EXECUTION D’UNE ATTAQUE
# ----------------------------------------------------
def executer_attaque(attaquant, cible, type_attaque, attaque_info):

    nom_fonction = attaque_info.get("fonction")
    module = __import__(__name__)

    if not hasattr(module, nom_fonction):
        raise ValueError(f"La fonction d’attaque '{nom_fonction}' n’existe pas dans attaques.py")

    fonction_attaque = getattr(module, nom_fonction)

    print(f"\n{attaquant.nom} utilise {attaque_info.get('nom','attaque inconnue')} !")

    # exécuter l’attaque
    degats_total = fonction_attaque(attaquant, cible)

    print(f"> {degats_total} dégâts infligés à {cible.nom} !")

    if not cible.est_vivant():
        print(f"{cible.nom} est mort !")
    attente = input("Appuyez sur Entrée pour continuer...")
    return degats_total

#  archer
def tir_rapide(attaquant, cible):
    degats = int(attaquant.atk * 0.75)
    reels = cible.prendre_degats(degats)
    return reels


def double_tir(attaquant, cible):
    total = 0
    for i in range(2):
        degats = int(attaquant.atk * 0.40)
        reels = cible.prendre_degats(degats)
        total += reels
        if not cible.est_vivant():
            break
    return total


def pluie_de_fleches(attaquant, cible):
    total = 0
    for i in range(10):
        pct = random.randint(20, 100)
        degats = int(attaquant.atk * (pct / 100))
        reels = cible.prendre_degats(degats)
        total += reels
        print(f"- Flèche {i+1} : {reels} dégats")

        if not cible.est_vivant():
            break
    return total


#  mage 

def arcane_simple(attaquant, cible):
    degats = int(attaquant.atk * 0.30)
    reels = cible.prendre_degats(degats)

    reduction = int(attaquant.atk * 0.10)
    cible.defense = max(0, cible.defense - reduction)

    print(f"> Défense de {cible.nom} réduite de {reduction} (nouvelle DEF : {cible.defense})")
    return reels


def fire_ball(attaquant, cible):
    degats = int(attaquant.atk * 0.70)
    reels = cible.prendre_degats(degats)

    print(f"> {cible.nom} est brûlé (5 dégâts / tour pendant 3 tours).")
    # effet brûlure à gérer dans Combattant.status_effects
    return reels


def mal_phenomenal(attaquant, cible):
    pv_manquants = cible.pv_max - cible.pv
    part_fixe = int(pv_manquants * 0.30)
    part_atk = int(attaquant.atk * 1.00)
    degats = part_fixe + part_atk

    reels = cible.prendre_degats(degats)
    return reels

# berserker

def hache_sauvage(attaquant, cible):
    degats = int(attaquant.atk * 0.80)
    reels = cible.prendre_degats(degats)
    return reels

def obtenir_attaques_disponibles(hero):

    attacks = []

    # attaque de base : toujours disponible
    attacks.append(("base", hero.attaques["base"]))

    # spé si pas en cooldown
    if hero.cooldowns.get("special", 0) == 0:
        attacks.append(("special", hero.attaques["special"]))

    # ulti si pas en cooldown
    if hero.cooldowns.get("ultime", 0) == 0:
        attacks.append(("ultime", hero.attaques["ultime"]))

    return attacks


def gerer_cooldown_attaque(hero, type_attaque, attaque_info):
    cooldown = attaque_info.get("cooldown", 0)

    if type_attaque == "special":
        hero.cooldowns["special"] = cooldown

    elif type_attaque == "ultime":
        hero.cooldowns["ultime"] = cooldown
