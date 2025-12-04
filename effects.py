

# effects.py


# EFFETS DE SOIN


def effet_soin(cible, montant):
    soins_reels = min(montant, cible.pv_max - cible.pv)
    cible.pv = min(cible.pv_max, cible.pv + soins_reels)
    print(f"> {cible.nom} récupère {soins_reels} PV (PV : {cible.pv}/{cible.pv_max})")
    return soins_reels


def effet_regen(cible, montant):
    soins_reels = min(montant, cible.pv_max - cible.pv)
    if soins_reels > 0:
        cible.pv += soins_reels
        print(f"{cible.nom} régénère {soins_reels} PV ! (PV : {cible.pv}/{cible.pv_max})")
    return soins_reels

def effet_vol_de_vie(degat, montant, attaquant):
    # montant est le pourcentage de regen en fonction des degats infligés
    soin = int(degat * (montant / 100))
    attaquant.pv = min(attaquant.pv_max, attaquant.pv + soin)
    print(f"> {attaquant.nom} vole {soin} PV ! (PV : {attaquant.pv}/{attaquant.pv_max})")
    return soin

# EFFETS DE BUFF

def buff_stat(cible, stat, montant, tours):
    # Applique le boost immédiatement
    if stat == "atk":
        cible.atk += montant
    elif stat == "defense":
        cible.defense += montant
    else:
        setattr(cible, stat, getattr(cible, stat) + montant)
    
    # Enregistre le buff dans la liste
    cible.buffs.append({
        "stat": stat,
        "montant": montant,
        "tours_restants": tours
    })
    
    nouvelle_valeur = getattr(cible, stat) if stat not in ["atk", "defense"] else (cible.atk if stat == "atk" else cible.defense)
    print(f"> {cible.nom} gagne +{montant} {stat} pour {tours} tours (nouvelle {stat.upper()} : {nouvelle_valeur})")


# EFFETS DE STATUS 

def brulure(cible, tours, montant=None):
    # Si pas de montant spécifié, utilise 5% des PV max
    if montant is None:
        montant = int(cible.pv_max * 0.05)
    
    cible.status.append({
        "stat": "brulure",
        "montant": montant,
        "tours_restants": tours
    })
    print(f" {cible.nom} est brûlé et subira {montant} dégâts pendant {tours} tours.")


def poison(cible, tours):
    montant = (cible.pv_max - cible.pv) / 100 *10
    
    montant = int(-(-montant // 1))
    cible.status.append({
        "stat": "poison",
        "montant": montant,
        "tours_restants": tours
    })
    print(f" {cible.nom} est empoisonné et subira {montant} dégâts pendant {tours} tours.")


def saignement(cible, tours, montant):
    montant = montant / 100 *10
    montant = int(-(-montant // 1))
    cible.status.append({
        "stat": "saignement",
        "montant": montant,
        "tours_restants": tours
    })
    print(f" {cible.nom} saigne et subira {montant} dégâts pendant {tours} tours.")



# EFFETS D'ITEMS SPÉCIAUX





    

