import random

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