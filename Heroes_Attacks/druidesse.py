from effects import transformation, poison, buff_stat, stun, effet_soin, creer_item
from db_init import get_db
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
        formes_druidesse = ["Loup", "Phénix", "Licorne"]
    
    formes_dispo = []
    for forme in formes_druidesse:
        forme_data = db.perso_annexe.find_one({"nom": forme})
        if forme_data:
            formes_dispo.append(forme_data)

    print("Choisissez une forme de transformation :")
    for id, forme in enumerate(formes_dispo, start=1):
        if forme["nom"] != attaquant.nom:
            print(f"{id}. \033[1m{forme['nom']}\033[0m - ATK:{forme['atk']} DEF:{forme['def']} PV:{forme['pv_max']}")
            print(f"forme {forme['type_perso']} Description : {forme['description']}")
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
    degats = int(attaquant.atk * 0.0)
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
    buff_stat(membre_aleatoire, stat_aleatoire, montant_boost, tours=9999)
    
    return 0

def invention(attaquant, cible, equipe):
        # Charger les taux de rareté
        # self.raretes = db.raretes.find_one({}, {"_id": 0}) or {}

        # # Charger tous les items
        # items = list(db.items.find({}, {"_id": 0}))

        # # Regrouper par rareté
        # items_par_rarete = {}
        # for item in items:
        #     r = item["rarete"]
        #     if r not in items_par_rarete:
        #         items_par_rarete[r] = []
        #     items_par_rarete[r].append(item)

        # self.items_par_rarete = items_par_rarete

        # charger les items et taux de rareté, les modifier en commun 70% et peut_commun 30%, puis créer un item aléatoire avec creer_item
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
