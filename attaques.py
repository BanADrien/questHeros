# === attaques.py ===

import random
from utils import afficher_equipe
from effects import effet_soin, buff_stat, brulure, effet_vol_de_vie, saignement, poison, effet_regen
from db_init import get_db
from models import Combattant



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


def transformation(attaquant, nouvelle_forme, equipe):
    db = get_db()
    
    forme_data = db.perso_annexe.find_one({"nom": nouvelle_forme})
    forme_data.pop("_id", None)
    
    forme_obj = Combattant(forme_data, est_heros=True)
    index = equipe.index(attaquant)
    print(f"> {attaquant.nom} se transforme en {forme_obj.nom} !")
    equipe[index] = forme_obj
    return 0
# spells pour chaque personnages 

#  archer
def tir_precis(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.75)
    reels = cible.prendre_degats_directs(degats)
    if attaquant.stack < 15:
        attaquant.stack += 1
    print(f">ignore la défense de {cible.nom} !")
    print(f"> flèche total stacké : {attaquant.stack})")
    return reels


def double_tir(attaquant, cible, equipe):
    total = 0
    for i in range(2):
        pct = random.randint(30, 70)
        degats = int(attaquant.atk * (pct / 100))
        reels = cible.prendre_degats(degats)
        total += reels
        if attaquant.stack < 15:
            attaquant.stack += 1
        if not cible.est_vivant():
            break
    
    print(f"> flèche total stacké : {attaquant.stack})")
    return total


def pluie_de_fleches(attaquant, cible, equipe):
    total = 0
    nombre_fleches = attaquant.stack
    for i in range(nombre_fleches):
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
    attaquant.atk += 1
    return reels


def fire_ball(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.70)
    reels = cible.prendre_degats(degats)

    brulure(cible, 3)
    
    attaquant.atk += 1
    return reels


def mal_phenomenal(attaquant, cible, equipe):
    pv_manquants = cible.pv_max - cible.pv
    part_fixe = int(pv_manquants * 0.30)
    part_atk = int(attaquant.atk * 1.00)
    degats = part_fixe + part_atk

    reels = cible.prendre_degats(degats)
    attaquant.atk += 1
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
    attaque = attaquant.atk * 0.25
    buff_stat(attaquant, "atk", int(attaque), 3)
    attaquant.stack += 2
    print(f"> {attaquant.nom} gagne {int(attaque)} points d'attaque (nouvelle ATK : {attaquant.atk}) pendant 2 tours et 2 stacks de rage (total : {attaquant.stack})")
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

def priere(attaquant, cible, equipe):
    soin_total = 0
    soin = 10
    for membre in equipe:
        membre.pv = min(membre.pv_max, membre.pv + soin)
        soin_total += soin
        print(f"> {membre.nom} récupère {soin} PV ")
    afficher_equipe(equipe)
    return 0

def benediction(attaquant, cible, equipe):
    
    montant_boost_def = int(attaquant.defense * 0.50)
    
    
    for membre in equipe:
        montant = int(membre.pv_max * 0.30)
        buff_stat(membre, "defense", montant_boost_def, 3)
        effet_soin(membre, montant)
    return 0
        
        
# hemomencien

def extraction_de_sang(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.50)
    reels = cible.prendre_degats(degats)
    soin = effet_vol_de_vie(reels, 50, attaquant)  
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

# chaman 

def totem_regen(attaquant, cible, equipe):
    for membre in equipe:
        effet_regen(membre, 5)
    return 0

def totem_brulure(attaquant, cible):
    brulure(cible, 3)
    return 0

def totem_poison(attaquant, cible):
    poison(cible, 3)
    return 0

def totem_degats(attaquant, cible):
    degats = int(attaquant.atk * 1.00)
    reels = cible.prendre_degats(degats)
    return reels

def totem(attaquant, cible, equipe):
    totems = [totem_regen, totem_brulure, totem_poison, totem_degats]
    totem_choisi = random.choice(totems)
    print(f"> Le totem invoqué est : {totem_choisi.__name__}")
    return totem_choisi(attaquant, cible, equipe)

def totem_de_guerre(attaquant, cible, equipe):
   
    for membre in equipe:
        montant_boost_atk = int(membre.atk * 0.30)
        buff_stat(membre, "atk", montant_boost_atk, 2)
    return 0

def totem_de_survie(attaquant, cible, equipe):
    montant_boost_def = 10
    montant_regen = 10
    for membre in equipe:
        buff_stat(membre, "defense", montant_boost_def, 3)
        effet_regen(membre, montant_regen)
        
        
    return 0

# villagois

def coup_de_fourche(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.50)
    reels = cible.prendre_degats(degats)
    return reels

def encouragement(attaquant, cible, equipe):
    for membre in equipe:
        # ne pas compter le villagois
        if membre != attaquant:
            for attaque in membre.cooldowns:
                if membre.cooldowns[attaque] > 0:
                    membre.cooldowns[attaque] = max(0, membre.cooldowns[attaque] - 1)
                    print(f"> Cooldown de l'attaque {attaque} de {membre.nom} réduit à {membre.cooldowns[attaque]}")
    return 0

def transformation_hero(attaquant, cible, equipe):
    
    transformation(attaquant, "Héro", equipe)
    
    return 0

# héro

    
def frappe_heroique(attaquant, cible, equipe):
    degats = int(attaquant.atk * 1.50)
    reels = cible.prendre_degats(degats)
    return reels

def motivation_du_hero(attaquant, cible, equipe):
    degats = int(attaquant.atk * 1)
    reels = cible.prendre_degats(degats)
    return reels

def transformation_legende(attaquant, cible, equipe):
    
    transformation(attaquant, "Légende", equipe)
    
    return 0


# légende
def frappe_legendaire(attaquant, cible, equipe):
    reels = frappe_heroique(attaquant, cible, equipe) 
    if cible.pv / cible.pv_max < 0.20:
        reels += cible.prendre_degats_directs(cible.pv)  
        print(f">{cible.nom} est instantanément tué !")
    return reels


def resurrection(attaquant, cible, equipe):
    membres_morts = [membre for membre in equipe if not membre.est_vivant()]
    if not membres_morts:
        print("Aucun membre mort à ressusciter.")
        return 0

    membre_a_ressusciter = random.choice(membres_morts)
    membre_a_ressusciter.pv = int(membre_a_ressusciter.pv_max)
    print(f"> {membre_a_ressusciter.nom} a été ressuscité")
    return 0

def aucun_rival(attaquant, cible, equipe):
    degats = int(cible.pv)
    reels = cible.prendre_degats_directs(degats)
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

