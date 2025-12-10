from effects import effet_vol_de_vie

def extraction_de_sang(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.60)
    reels = cible.prendre_degats(degats)
    soin, msg_vol = effet_vol_de_vie(reels, attaquant)  # Décomposer le tuple
    attaquant.stack += soin
    
    return {
        "degats": reels,
        "messages": [
            msg_vol,
            f"{attaquant.nom} gagne {soin} stacks (total: {attaquant.stack})"
        ]
    }

def explosion_sanguine(attaquant, cible, equipe):
    degats = int(attaquant.stack)
    reels = cible.prendre_degats(degats)
    stacks_utilises = attaquant.stack
    attaquant.stack = 0
    
    return {
        "degats": reels,
        "messages": [f"{attaquant.nom} utilise {stacks_utilises} stacks pour infliger {reels} dégâts !"]
    }

def siphonage_total(attaquant, cible, equipe):
    degats = int(attaquant.atk * 2.00)
    reels = cible.prendre_degats(degats)
    soin, msg_vol = effet_vol_de_vie(reels, attaquant)  # Décomposer le tuple
    attaquant.stack += soin
    
    return {
        "degats": reels,
        "messages": [
            msg_vol,
            f"{attaquant.nom} gagne {soin} stacks (total: {attaquant.stack})"
        ]
    }