# === attaques.py ===

import random
from utils import afficher_equipe
from effects import effet_soin, buff_stat, brulure, effet_vol_de_vie, saignement, poison


def executer_attaque(attaquant, cible, equipe, type_attaque, attaque_info):

    nom_fonction = attaque_info.get("fonction")
    module = __import__(__name__)

    if not hasattr(module, nom_fonction):
        raise ValueError(f"La fonction d’attaque '{nom_fonction}' n’existe pas dans attaques.py")

    fonction_attaque = getattr(module, nom_fonction)

    print(f"\n{attaquant.nom} utilise {attaque_info.get('nom','attaque inconnue')} !")

    # exécuter l’attaque
    degats_total = fonction_attaque(attaquant, cible, equipe)
    if degats_total > 0:
        print(f"> {degats_total} dégâts infligés à {cible.nom} !")

    if not cible.est_vivant():
        print(f"{cible.nom} est mort !")
    return degats_total


    
# spells pour chaque personnages 

#  archer
def tir_precis(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.75)
    reels = cible.prendre_degats_directs(degats)
    print(f">ignore la défense de {cible.nom} !")
    return reels


def double_tir(attaquant, cible, equipe):
    total = 0
    for i in range(2):
        pct = random.randint(30, 70)
        degats = int(attaquant.atk * (pct / 100))
        reels = cible.prendre_degats(degats)
        total += reels
        if not cible.est_vivant():
            break
    return total


def pluie_de_fleches(attaquant, cible, equipe):
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

def arcane_simple(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.30)
    reels = cible.prendre_degats(degats)

    reduction = int(attaquant.atk * 0.10)
    cible.defense = max(0, cible.defense - reduction)

    print(f"> Défense de {cible.nom} réduite de {reduction} (nouvelle DEF : {cible.defense})")
    return reels


def fire_ball(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.70)
    reels = cible.prendre_degats(degats)

    brulure(cible, 3)
    
    # effet brûlure à gérer dans Combattant.status_effects
    return reels


def mal_phenomenal(attaquant, cible, equipe):
    pv_manquants = cible.pv_max - cible.pv
    part_fixe = int(pv_manquants * 0.30)
    part_atk = int(attaquant.atk * 1.00)
    degats = part_fixe + part_atk

    reels = cible.prendre_degats(degats)
    return reels

# berserker

def hache_sauvage(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.80)
    reels = cible.prendre_degats(degats)
    attaquant.stack += 1
    print(f"> {attaquant.nom} gagne 1 stack de rage (total : {attaquant.stack})")
    return reels

def echauffement(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.20)
    reels = cible.prendre_degats(degats)
    #  commme la brulure rajouter une fonction d'effet de boost
    attaquant.atk += 5  
    attaquant.stack += 2
    print(f"> {attaquant.nom} gagne 5 points d'attaque (nouvelle ATK : {attaquant.atk}) et 2 stacks de rage (total : {attaquant.stack})")
    return reels

def dechainement_totale(attaquant, cible, equipe):
    degats = int(attaquant.atk * (1.00 * attaquant.stack))
    reels = cible.prendre_degats(degats)
    print(f"> {attaquant.nom} utilise {attaquant.stack} stacks de rage pour augmenter les dégâts !")
    attaquant.stack = 0  
    return reels

# paladin

def coup_de_bouclier(attaquant, cible, equipe):
    degats = int(attaquant.pv_max * 0.15)
    reels = cible.prendre_degats(degats)
    return reels

def benediction(attaquant, cible, equipe):
    soin_total = 0
    for membre in equipe:
        pv_manquants = membre.pv_max - membre.pv
        soin = int(pv_manquants * 0.20)
        membre.pv = min(membre.pv_max, membre.pv + soin)
        soin_total += soin
        print(f"> {membre.nom} récupère {soin} PV ")
    afficher_equipe(equipe)
    return 0

def chatiment(attaquant, cible, equipe):
    
    montant_boost_def = int(attaquant.defense * 0.50)
    
    
    for membre in equipe:
        montant = int((membre.pv_max - membre.pv) * 0.30)
        buff_stat(membre, "defense", montant_boost_def, 3)
        effet_soin(membre, montant)
    return 0
        
        
# hemomencien

def extraction_de_sang(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.60)
    reels = cible.prendre_degats(degats)
    soin = effet_vol_de_vie(reels, 30, attaquant)  
    attaquant.stack += soin
    print(f" points de stack total: {attaquant.stack}")
    return reels

def explosion_sanguine(attaquant, cible, equipe):
    degats = int(attaquant.stack)
    reels = cible.prendre_degats(degats)
    attaquant.stack = 0
    return reels

def siphonage_total(attaquant, cible, equipe):
    degats = int(attaquant.atk * 2.00)
    reels = cible.prendre_degats(degats)
    soin = effet_vol_de_vie(reels, 100, attaquant)  
    attaquant.stack += soin
    return reels

# Assassin

def incision (attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.50)
    reels = cible.prendre_degats(degats)
    saignement(cible, 3, reels)  
    return reels

def lame_toxique (attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.80)
    reels = cible.prendre_degats(degats)
    poison(cible, 3) 
    
    return reels

def assassinat (attaquant, cible, equipe):
    degats = int(attaquant.atk * 2.00)
    reels = cible.prendre_degats(degats)
    if cible.pv / cible.pv_max < 0.20:
        reels += cible.prendre_degats_directs(cible.pv)  
        print(f">{cible.nom} est instantanément tué !")
    return reels


def obtenir_attaques_disponibles(hero):
    return [
        ("base", hero.attaques["base"]),
        ("special", hero.attaques["special"]),
        ("ultime", hero.attaques["ultime"])
    ]



def gerer_cooldown_attaque(hero, type_attaque, attaque_info):
    cooldown = attaque_info.get("cooldown", 0)

    if cooldown > 0:
        hero.cooldowns[type_attaque] = cooldown + 1
        print(f"> {hero.nom} met {type_attaque} en cooldown pour {cooldown} tours.")

