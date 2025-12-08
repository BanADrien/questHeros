from effects import transformation, poison, buff_stat, stun, effet_soin, creer_item, brulure, ressuciter_avec_choix, effet_regen, saignement, prendre_focus, buff_stat_definitif
from db_init import get_db
from utils import choix_perso
import random
def methamorphose(attaquant, cible, equipe):
    # faire choisir une forme
    db = get_db()
    attaquant.stack += 1

    print(f"> la druidesse gagne 1 stack de transformation (total : {attaquant.stack})")
    if attaquant.stack < 5:
        formes_druidesse = ["Arraignée géante", "Tortue blindée", "Singe savant"]
    else : 
        print("La druidesse peut maintenant se transformer en bête mythique!")
        formes_druidesse = ["Fenrir", "Phoenix", "Golem antique"]
    
    formes_dispo = []
    for forme in formes_druidesse:
        
        forme_data = db.perso_annexe.find_one({"nom": forme})
        if forme_data and forme_data.get("nom") != attaquant.nom:
            formes_dispo.append(forme_data)

    print("Choisissez une forme de transformation :")
    
           
    choix_perso(formes_dispo)
    choix = input("Entrez le numéro de la forme choisie : ")
    try:
        choix_int = int(choix)
        if 1 <= choix_int <= len(formes_dispo):
            forme_choisie = formes_dispo[choix_int - 1]["nom"]
            transformation(attaquant, forme_choisie, equipe)
        else:
            print("Choix invalide.")
    except ValueError:
        print("Entrée invalide.")
    return 0

# arraigée géante

def dard_venimeux(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.80)
    reels = cible.prendre_degats(degats)
    poison(cible, 3)
    return reels

def paralysie(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.20)
    reels = cible.prendre_degats(degats)
    stun(cible, 2)
    return reels

# torute blindée

def auto_guerison(attaquant, cible, equipe):
    soin = 30
    effet_soin(attaquant, soin)
    return 0

def carapace_partagee(attaquant, cible, equipe):
    montant_def = 30
    for membre in equipe:
        buff_stat(membre, "defense", montant_def, 3)
    return 0

# singe savant

def cours_particulier(attaquant, cible, equipe):
    #donne 5 point d'une stat definitivement aléatoire à un allié aléatoire
    stat_aleatoire = random.choice(["atk", "defense", "pv_max"])
    # ne pas choisir soi meme
    equipe_sans_attaquant = [membre for membre in equipe if membre != attaquant]
    membre_aleatoire = random.choice(equipe_sans_attaquant)
    montant_boost = 5
    buff_stat_definitif(membre_aleatoire, stat_aleatoire, montant_boost)
    
    return 0

def invention(attaquant, cible, equipe):
     
    db = get_db()
    raretes = {'commun': 70, 'peu_commun': 30}
    items_par_rarete = {}
    
    items = list(db.items.find({}, {"_id": 0}))
    for item in items:
        r = item["rarete"]
        if r not in items_par_rarete:
            items_par_rarete[r] = []
        items_par_rarete[r].append(item)
        
   
    creer_item(attaquant, equipe, raretes, items_par_rarete)
        
    return 0


# phoenix

def feu_sacre(attaquant, cible, equipe):
    degats = int(attaquant.atk * 1.00)
    reels = cible.prendre_degats(degats)
    brulure(cible, 5)
    return reels

def feu_resurecteur(attaquant, cible, equipe):
    ressuciter_avec_choix(attaquant, equipe)
    for membre in equipe:
        effet_regen(membre, 10)
        
# fenrir

def dechiquetage(attaquant, cible, equipe):
    degats = int(attaquant.atk * 1.50)
    reels = cible.prendre_degats(degats)
    saignement(cible, reels, 5)
    return reels
    
def hurlement(attaquant, cible, equipe):
    stun(cible, 2)
    return 0

# golem antique

def frappe_sismique(attaquant, cible, equipe):
    degats = int(attaquant.defense * 0.50)
    reels = cible.prendre_degats(degats)
    prendre_focus(attaquant, cible, tours=2)
    
    return reels


def inflexible(attaquant, cible, equipe):
    montant_def = 30
    montant_pv = attaquant.pv_max * 0.30
    buff_stat(attaquant, "defense", montant_def, 3)
    effet_soin(attaquant, montant_pv)
    return 0
