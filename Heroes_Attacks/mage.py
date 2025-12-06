from effects import brulure

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
