from effects import transformation, buff_stat, resurrection, ressuciter_avec_choix


def coup_de_fourche(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.50)
    reels = cible.prendre_degats(degats)
    return {"degats": reels, "messages": []}

def encouragement(attaquant, cible, equipe):
    messages = []
    for membre in equipe:
        # ne pas compter le villageois
        if membre != attaquant:
            for attaque in membre.cooldowns:
                if membre.cooldowns[attaque] > 0:
                    membre.cooldowns[attaque] = max(0, membre.cooldowns[attaque] - 1)
                    messages.append(f"Cooldown de {attaque} de {membre.nom} réduit à {membre.cooldowns[attaque]}")
    
    if not messages:
        messages.append("Aucun cooldown à réduire.")
    
    return {"degats": 0, "messages": messages}

def transformation_hero(attaquant, cible, equipe):
    _, msg = transformation(attaquant, "Héro", equipe)
    return {"degats": 0, "messages": [msg]}

# =========================== héro
    
def frappe_heroique(attaquant, cible, equipe):
    degats = int(attaquant.atk * 1.20)
    reels = cible.prendre_degats(degats)
    return {"degats": reels, "messages": []}

def motivation_du_hero(attaquant, cible, equipe):
    montant_atk = int(attaquant.atk * 0.20)
    montant_def = int(attaquant.defense * 0.20)
    messages = []
    
    for membre in equipe:
        if membre != attaquant:
            _, msg_atk = buff_stat(membre, "atk", montant_atk, 2)
            messages.append(msg_atk)
            
            _, msg_def = buff_stat(membre, "defense", montant_def, 2)
            messages.append(msg_def)
            
            # réduire cooldown de 1
            for attaque in membre.cooldowns:    
                if membre.cooldowns[attaque] > 0:
                    membre.cooldowns[attaque] = max(0, membre.cooldowns[attaque] - 1)
                    messages.append(f"Cooldown de {attaque} de {membre.nom} réduit à {membre.cooldowns[attaque]}")
    
    return {"degats": 0, "messages": messages}

def transformation_legende(attaquant, cible, equipe):
    _, msg = transformation(attaquant, "Légende", equipe)
    return {"degats": 0, "messages": [msg]}


# =========================== légende

def frappe_legendaire(attaquant, cible, equipe):
    messages = []
    degats = int(attaquant.atk * 1.20)
    reels = cible.prendre_degats(degats)
    
    if cible.pv / cible.pv_max < 0.20:
        degats_exec = cible.prendre_degats_directs(cible.pv)
        reels += degats_exec
        messages.append(f"{cible.nom} est instantanément exécuté !")
    
    return {"degats": reels, "messages": messages}


def motivation_legendaire(attaquant, cible, equipe):
    messages = []
    
    # Motivation du héro
    result_motiv = motivation_du_hero(attaquant, cible, equipe)
    messages.extend(result_motiv["messages"])
    
    # Résurrection
    _, msg_res = ressuciter_avec_choix(attaquant, equipe)
    messages.append(msg_res)
    
    return {"degats": 0, "messages": messages}

def aucun_rival(attaquant, cible, equipe):
    degats = int(cible.pv)
    reels = cible.prendre_degats_directs(degats)
    return {"degats": reels, "messages": [f"{cible.nom} reçoit des dégâts égaux à ses PV restants !"]}