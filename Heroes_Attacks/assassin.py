from effects import saignement, poison
def incision (attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.50)
    reels = cible.prendre_degats(degats)
    saignement(cible, reels, 3)  
    return reels

def lame_toxique (attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.60)
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