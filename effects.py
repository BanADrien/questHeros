from db_init import get_db
from models import Combattant
from items import generer_loot, choisir_rarete, obtenir_item
# effects.py


# EFFETS DE SOIN


def effet_soin(cible, montant):
    soins_reels = min(montant, cible.pv_max - cible.pv)
    cible.pv = min(cible.pv_max, cible.pv + soins_reels)
    # Retourner le montant et un message
    return soins_reels, f"{cible.nom} récupère {soins_reels} PV (PV : {cible.pv}/{cible.pv_max})"


def effet_regen(cible, montant, tours=3):
    soin = 0-montant
    cible.status.append({
        "stat": "regen",
        "montant": soin,
        "tours_restants": tours,
    })
    return 0, f"{cible.nom} bénéficiera de {-soin} pv de régénération pendant {tours} tours."

def effet_vol_de_vie(degat, attaquant):
    # montant est le pourcentage de regen en fonction des degats infligés
    soin = int(degat * 0.30)
    attaquant.pv = min(attaquant.pv_max, attaquant.pv + soin)
    return soin, f"{attaquant.nom} vole {soin} PV ! (PV : {attaquant.pv}/{attaquant.pv_max})"

def resurrection(cible):
    if cible.est_vivant():
        return False, f"{cible.nom} est déjà vivant et ne peut pas être ressuscité."
    
    cible.pv = cible.pv_max // 2  # Ressusciter avec la moitié des PV max
    return True, f"{cible.nom} a été ressuscité avec {cible.pv} PV !"

def ressuciter_avec_choix(attaquant, equipe):

    membres_morts = [membre for membre in equipe if not membre.est_vivant()]
    
    if len(membres_morts) >= 1:
        # Ressuscite le premier membre mort
        membre_a_ressusciter = membres_morts[0]
        success, msg = resurrection(membre_a_ressusciter)
        return 0, msg
    
    return 0, "Aucun membre mort à ressusciter."

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
    return 0, f"{cible.nom} gagne +{montant} {stat} pour {tours} tours (nouvelle {stat.upper()} : {nouvelle_valeur})"

def buff_stat_definitif(cible, stat, montant):
    if stat == "atk":
        cible.atk += montant
    elif stat == "defense":
        cible.defense += montant
    elif stat == "pv_max":
        cible.pv_max += montant
        cible.pv += montant  
    else:
        setattr(cible, stat, getattr(cible, stat) + montant)
    
    nouvelle_valeur = getattr(cible, stat) if stat not in ["atk", "defense"] else (cible.atk if stat == "atk" else cible.defense)
    return 0, f"{cible.nom} gagne définitivement +{montant} {stat} (nouvelle {stat.upper()} : {nouvelle_valeur})"

# EFFETS DE STATUS 

def brulure(cible, tours):
    # Si pas de montant spécifié, utilise 5% des PV max
    montant = int(cible.pv_max * 0.05)
    
    cible.status.append({
        "stat": "brulure",
        "montant": montant,
        "tours_restants": tours
    })
    return 0, f"{cible.nom} est brûlé et subira {montant} dégâts pendant {tours} tours."


def poison(cible, tours):
    montant = (cible.pv_max - cible.pv) / 100 *10
    montant = int(-(-montant // 1))
    cible.status.append({
        "stat": "poison",
        "montant": montant,
        "tours_restants": tours
    })
    return 0, f"{cible.nom} est empoisonné et subira {montant} dégâts pendant {tours} tours."


def saignement(cible, montant, tours):
    degats_saignement = int(montant * 0.15)
    cible.status.append({
        "stat": "saignement",
        "montant": degats_saignement,
        "tours_restants": tours
    })
    return 0, f"{cible.nom} saigne et subira {degats_saignement} dégâts pendant {tours} tours."

def stun(cible, tours):
    cible.status.append({
        "stat": "stun",
        "montant": 1,
        "tours_restants": tours
    })
    return 0, f"{cible.nom} est étourdi et ne pourra pas agir pendant {tours-1} tours."

# EFFETS Speciaux
def creer_item(attaquant, equipe, rarete_list, items_par_rarete):
    """Génère un item et remonte les infos pour ouvrir l'écran de choix"""
    item = obtenir_item(equipe, rarete_list, items_par_rarete)
    if item:
        return {
            "degats": 0,
            "messages": [f"Un item {item.nom} ({item.rarete}) a été créé !"],
            "ouvrir_selection_item": True,
            "item_cree": item,
        }
    return {"degats": 0, "messages": ["Aucun item n'a été créé."]}
    
def transformation(attaquant, nouvelle_forme, equipe):
    db = get_db()
    
    forme_data = db.perso_annexe.find_one({"nom": nouvelle_forme})
    if not forme_data:
        return 0, f"Forme {nouvelle_forme} non trouvée."
    
    forme_data.pop("_id", None)
    
    sauver_stack = attaquant.stack
    sauver_vie = attaquant.pv
    sauver_items = attaquant.items
    
    forme_obj = Combattant(forme_data, est_heros=True)
    
    forme_obj.stack = sauver_stack
    forme_obj.pv = min(sauver_vie, forme_obj.pv_max)
    forme_obj.items = sauver_items
    
    index = equipe.index(attaquant)
    ancien_nom = attaquant.nom
    equipe[index] = forme_obj
    
    return 0, f"{ancien_nom} se transforme en {forme_obj.nom} !"

def prendre_focus(attaquant, cible, tours=1):
    attaquant.status.append({
        "stat": "prendre_focus",
        "montant": 1,
        "tours_restants": tours,
    })
    return 0, f"{cible.nom} prend le focus des attaques ennemies pour {tours} tours !"