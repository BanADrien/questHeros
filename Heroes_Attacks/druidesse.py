from effects import transformation, poison, buff_stat, stun
from db_init import get_db
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
    degats = int(attaquant.atk * 0.10)
    reels = cible.prendre_degats(degats)
    stun(cible, 2)
    return reels