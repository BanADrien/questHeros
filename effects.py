
from db_init import get_db
from models import Combattant
from items import generer_loot, choisir_rarete, obtenir_item
# effects.py


# EFFETS DE SOIN


def effet_soin(cible, montant):
    soins_reels = min(montant, cible.pv_max - cible.pv)
    cible.pv = min(cible.pv_max, cible.pv + soins_reels)
    print(f"> {cible.nom} récupère {soins_reels} PV (PV : {cible.pv}/{cible.pv_max})")
    return soins_reels


def effet_regen(cible, montant):
    montant = 0-montant
    cible.status.append({
        "stat": "regen",
        "montant": montant,
        "tours_restants": 3,
    })
    print(f" {cible.nom} bénéficiera de {-montant} pv de régénération pendant 3 tours.")

def effet_vol_de_vie(degat, montant, attaquant):
    # montant est le pourcentage de regen en fonction des degats infligés
    soin = int(degat * (montant / 100))
    attaquant.pv = min(attaquant.pv_max, attaquant.pv + soin)
    print(f"> {attaquant.nom} vole {soin} PV ! (PV : {attaquant.pv}/{attaquant.pv_max})")
    return soin

def resurrection(cible):
    
    if cible.est_vivant():
        print(f"> {cible.nom} est déjà vivant et ne peut pas être ressuscité.")
        return False
    
    cible.pv = cible.pv_max // 2  # Ressusciter avec la moitié des PV max
    print(f"> {cible.nom} a été ressuscité avec {cible.pv} PV !")
    return True

def ressuciter_avec_choix(attaquant, equipe):
    membres_morts = [membre for membre in equipe if not membre.est_vivant()]
    if len(membres_morts) == 1:
        membre_a_ressusciter = membres_morts[0]
        resurrection(membre_a_ressusciter)
        print(f"> {membre_a_ressusciter.nom} a été ressuscité")
        return 0
    elif len(membres_morts) > 1:
        print("> Membres morts disponibles pour la résurrection :")
        for idx, membre in enumerate(membres_morts, start=1):
            print(f"{idx}. {membre.nom}")
        while True:
            try:
                choix = int(input("Choisissez un membre à ressusciter (numéro) : "))
                if 1 <= choix <= len(membres_morts):
                    membre_a_ressusciter = membres_morts[choix - 1]
                    resurrection(membre_a_ressusciter)
                    print(f"> {membre_a_ressusciter.nom} a été ressuscité")
                    return 0
                else:
                    print("Choix invalide. Veuillez réessayer.")
            except ValueError:
                print("Entrée invalide. Veuillez entrer un numéro.")
    else :
        print("> Aucun membre mort à ressusciter.")
    return 0

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
    montant = montant * 0.15
    montant = int(-(-montant // 1))
    cible.status.append({
        "stat": "saignement",
        "montant": montant,
        "tours_restants": tours
    })
    print(f" {cible.nom} saigne et subira {montant} dégâts pendant {tours} tours.")

def stun(cible, tours):
    cible.status.append({
        "stat": "stun",
        "montant": 1,
        "tours_restants": tours
    })
    print(f" {cible.nom} est étourdi et ne pourra pas agir pendant {tours-1} tours.")
# EFFETS Speciaux
def creer_item(attaquant, equipe, rarete_list, items_par_rarete):
    # obtenir_item(attaquant, nom_item)
    item = obtenir_item(equipe, rarete_list, items_par_rarete)
    
def transformation(attaquant, nouvelle_forme, equipe):
    db = get_db()
    
    forme_data = db.perso_annexe.find_one({"nom": nouvelle_forme})
    forme_data.pop("_id", None)
    
    forme_obj = Combattant(forme_data, est_heros=True)
    index = equipe.index(attaquant)
    print(f"> {attaquant.nom} se transforme en {forme_obj.nom} !")
    equipe[index] = forme_obj
    return 0

def prendre_focus(attaquant, cible, tours=1):
    attaquant.status.append({
        "stat": "prendre_focus",
        "montant": 1,
        "tours_restants": tours,
    })
    print(f"> {cible.nom} prend le focus des attaques ennemies pour {tours} tours !")
    return 0




    

