from effects import effet_vol_de_vie
def extraction_de_sang(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.50)
    reels = cible.prendre_degats(degats)
    soin = effet_vol_de_vie(reels, attaquant)  
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
    soin = effet_vol_de_vie(reels, attaquant)  
    attaquant.stack += soin
    return reels
