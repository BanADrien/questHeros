from effects import transformation, poison, buff_stat, stun, effet_soin, creer_item, brulure, ressuciter_avec_choix, effet_regen, saignement, prendre_focus, buff_stat_definitif
from db_init import get_db
import random

def methamorphose(attaquant, cible, equipe):
    """
    VERSION GUI : Retourne les infos pour ouvrir l'écran de sélection
    Le combat gérera l'ouverture de l'écran de sélection
    """
    db = get_db()
    attaquant.stack += 1
    messages = [f"La druidesse gagne 1 stack de transformation (total : {attaquant.stack})"]

    if attaquant.stack < 5:
        formes_druidesse = ["Arraignée géante", "Tortue blindée", "Singe savant"]
    else: 
        messages.append("La druidesse peut maintenant se transformer en bête mythique!")
        formes_druidesse = ["Fenrir", "Phoenix", "Golem antique"]
    
    formes_dispo = []
    for forme in formes_druidesse:
        forme_data = db.perso_annexe.find_one({"nom": forme})
        if forme_data and forme_data.get("nom") != attaquant.nom:
            formes_dispo.append(forme_data["nom"])

    if not formes_dispo:
        messages.append("Aucune forme disponible pour la transformation.")
        return {"degats": 0, "messages": messages}
    
    # Retourner un format spécial pour demander la sélection de forme
    return {
        "degats": 0, 
        "messages": messages,
        "selection_forme": True,  # Flag pour indiquer qu'il faut ouvrir l'écran de sélection
        "formes_disponibles": formes_dispo
    }

# arraignée géante

def dard_venimeux(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.80)
    reels = cible.prendre_degats(degats)
    _, msg = poison(cible, 3)
    return {"degats": reels, "messages": [msg]}

def paralysie(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.20)
    reels = cible.prendre_degats(degats)
    _, msg = stun(cible, 2)
    return {"degats": reels, "messages": [msg]}

# tortue blindée

def auto_guerison(attaquant, cible, equipe):
    soin = 30
    soins_reels, msg = effet_soin(attaquant, soin)
    return {"degats": 0, "messages": [msg]}

def carapace_partagee(attaquant, cible, equipe):
    montant_def = 30
    messages = []
    for membre in equipe:
        _, msg = buff_stat(membre, "defense", montant_def, 3)
        messages.append(msg)
    return {"degats": 0, "messages": messages}

# singe savant

def cours_particulier(attaquant, cible, equipe):
    # donne 5 points d'une stat définitivement aléatoire à un allié aléatoire
    stat_aleatoire = random.choice(["atk", "defense", "pv_max"])
    # ne pas choisir soi-même
    equipe_sans_attaquant = [membre for membre in equipe if membre != attaquant]
    if not equipe_sans_attaquant:
        return {"degats": 0, "messages": ["Aucun allié disponible pour le cours particulier."]}
    
    membre_aleatoire = random.choice(equipe_sans_attaquant)
    montant_boost = 5
    _, msg = buff_stat_definitif(membre_aleatoire, stat_aleatoire, montant_boost)
    
    return {"degats": 0, "messages": [msg]}

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
    
    resultat = creer_item(attaquant, equipe, raretes, items_par_rarete)
    return resultat

# phoenix

def feu_sacre(attaquant, cible, equipe):
    degats = int(attaquant.atk * 1.00)
    reels = cible.prendre_degats(degats)
    _, msg = brulure(cible, 5)
    return {"degats": reels, "messages": [msg]}

def feu_resurecteur(attaquant, cible, equipe):
    messages = []
    _, msg_res = ressuciter_avec_choix(attaquant, equipe)
    messages.append(msg_res)
    
    for membre in equipe:
        _, msg_regen = effet_regen(membre, 10, 3)
        messages.append(msg_regen)
    
    return {"degats": 0, "messages": messages}

# fenrir

def dechiquetage(attaquant, cible, equipe):
    degats = int(attaquant.atk * 1.50)
    reels = cible.prendre_degats(degats)
    _, msg = saignement(cible, reels, 5)
    return {"degats": reels, "messages": [msg]}
    
def hurlement(attaquant, cible, equipe):
    _, msg = stun(cible, 2)
    return {"degats": 0, "messages": [msg]}

# golem antique

def frappe_sismique(attaquant, cible, equipe):
    degats = int(attaquant.defense * 0.50)
    reels = cible.prendre_degats(degats)
    _, msg = prendre_focus(attaquant, cible, tours=2)
    return {"degats": reels, "messages": [msg]}

def inflexible(attaquant, cible, equipe):
    montant_def = 30
    montant_pv = int(attaquant.pv_max * 0.30)
    
    messages = []
    _, msg_def = buff_stat(attaquant, "defense", montant_def, 3)
    messages.append(msg_def)
    
    soins_reels, msg_soin = effet_soin(attaquant, montant_pv)
    messages.append(msg_soin)
    
    return {"degats": 0, "messages": messages}