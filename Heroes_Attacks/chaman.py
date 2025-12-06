from effects import buff_stat, effet_regen, brulure, poison
import random


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