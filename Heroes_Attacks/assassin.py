from effects import saignement, poison

def incision(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.50)
    reels = cible.prendre_degats(degats)
    _, msg = saignement(cible, reels, 3)
    
    return {
        "degats": reels,
        "messages": [msg]
    }

def lame_toxique(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.60)
    reels = cible.prendre_degats(degats)
    _, msg = poison(cible, 3)
    
    return {
        "degats": reels,
        "messages": [msg]
    }

def assassinat(attaquant, cible, equipe):
    degats = int(attaquant.atk * 2.00)
    reels = cible.prendre_degats(degats)
    messages = []
    
    if cible.pv / cible.pv_max < 0.20:
        reels += cible.prendre_degats_directs(cible.pv)
        messages.append(f"{cible.nom} est instantanément tué !")
    
    return {
        "degats": reels,
        "messages": messages
    }