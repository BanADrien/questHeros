from effects import buff_stat, effet_soin
def coup_de_bouclier(attaquant, cible, equipe):
    degats = int(attaquant.pv_max * 0.15)
    reels = cible.prendre_degats(degats)
    return reels

def priere(attaquant, cible, equipe):
    soin_total = 0
    soin = 10
    for membre in equipe:
        membre.pv = min(membre.pv_max, membre.pv + soin)
        soin_total += soin
        print(f"> {membre.nom} récupère {soin} PV ")
    return 0

def benediction(attaquant, cible, equipe):
    
    montant_boost_def = int(attaquant.defense * 0.50)
    
    
    for membre in equipe:
        montant = int(membre.pv_max * 0.30)
        buff_stat(membre, "defense", montant_boost_def, 3)
        effet_soin(membre, montant)
    return 0