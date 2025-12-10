from effects import buff_stat
def hache_sauvage(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.80)
    reels = cible.prendre_degats(degats)
    attaquant.stack += 1
    messages = [f"{attaquant.nom} gagne 1 stack de rage (total : {attaquant.stack})"]
    return {"degats": reels, "messages": messages}

def echauffement(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.20)
    reels = cible.prendre_degats(degats)
    attaque = attaquant.atk * 0.25
    _, msg_buff = buff_stat(attaquant, "atk", int(attaque), 3)
    attaquant.stack += 2
    messages = [msg_buff, f"{attaquant.nom} gagne 2 stacks de rage (total : {attaquant.stack})"]
    return {"degats": reels, "messages": messages}

def dechainement_totale(attaquant, cible, equipe):
    degats = int(attaquant.atk * (1.00 * attaquant.stack))
    reels = cible.prendre_degats(degats)
    messages = [f"{attaquant.nom} utilise {attaquant.stack} stacks de rage pour augmenter les dégâts !"]
    attaquant.stack = 0  
    return {"degats": reels, "messages": messages}