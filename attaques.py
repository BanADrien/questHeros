# === attaques.py ===

import random
from effects import effet_soin, buff_stat, brulure, effet_vol_de_vie, saignement, poison, effet_regen, resurrection
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



#==================== spells pour chaque personnages ========================

# =========================== archer
from Heroes_Attacks.archer import tir_precis, double_tir, pluie_de_fleches


# =========================== mage 
from Heroes_Attacks.mage import arcane_simple, fire_ball, mal_phenomenal


# =========================== berserker
from Heroes_Attacks.berserker import hache_sauvage, echauffement, dechainement_totale


# =========================== paladin
from Heroes_Attacks.paladin import coup_de_bouclier, priere, benediction
        
        
# =========================== hemomencien
from Heroes_Attacks.hemomencien import extraction_de_sang, explosion_sanguine, siphonage_total


# =========================== Assassin
from Heroes_Attacks.assassin import incision, lame_toxique, assassinat


# =========================== chaman 
from Heroes_Attacks.chaman import totem, totem_de_guerre, totem_de_survie

# =========================== villageois
from Heroes_Attacks.villagois import coup_de_fourche, encouragement, transformation_hero, frappe_heroique, motivation_du_hero, transformation_legende, frappe_legendaire, motivation_legendaire, aucun_rival

# =========================== druidesse
from Heroes_Attacks.druidesse import methamorphose, dard_venimeux, paralysie












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

