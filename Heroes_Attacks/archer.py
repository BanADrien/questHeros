import random

def tir_precis(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.75)
    reels = cible.prendre_degats_directs(degats)
    if attaquant.stack < 15:
        attaquant.stack += 1
    messages = [f"{cible.nom} n'ignore pas la défense !", f"Flèche totale stackée : {attaquant.stack}"]
    return {"degats": reels, "messages": messages}


def double_tir(attaquant, cible, equipe):
    total = 0
    messages = []
    for i in range(2):
        pct = random.randint(30, 70)
        degats = int(attaquant.atk * (pct / 100))
        reels = cible.prendre_degats(degats)
        total += reels
        messages.append(f"Flèche {i+1} : {reels} dégâts")
        if attaquant.stack < 15:
            attaquant.stack += 1
        if not cible.est_vivant():
            break
    
    messages.append(f"Flèche totale stackée : {attaquant.stack}")
    return {"degats": total, "messages": messages}


def pluie_de_fleches(attaquant, cible, equipe):
    total = 0
    nombre_fleches = attaquant.stack
    messages = []
    for i in range(nombre_fleches):
        pct = random.randint(20, 100)
        degats = int(attaquant.atk * (pct / 100))
        reels = cible.prendre_degats(degats)
        total += reels
        messages.append(f"Flèche {i+1} : {reels} dégâts")

        if not cible.est_vivant():
            break
    return {"degats": total, "messages": messages}