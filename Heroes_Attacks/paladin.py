from effects import buff_stat, effet_soin
def coup_de_bouclier(attaquant, cible, equipe):
    degats = int(attaquant.pv_max * 0.15)
    reels = cible.prendre_degats(degats)
    return {"degats": reels, "messages": []}

def priere(attaquant, cible, equipe):
    messages = []
    soin = 10
    for membre in equipe:
        soins_reels, msg = effet_soin(membre, soin)
        messages.append(msg)
    return {"degats": 0, "messages": messages}

def benediction(attaquant, cible, equipe):
    montant_boost_def = int(attaquant.defense * 0.50)
    messages = []
    
    for membre in equipe:
        montant = int(membre.pv_max * 0.30)
        _, msg_def = buff_stat(membre, "defense", montant_boost_def, 3)
        messages.append(msg_def)
        soins_reels, msg_soin = effet_soin(membre, montant)
        messages.append(msg_soin)
    return {"degats": 0, "messages": messages}