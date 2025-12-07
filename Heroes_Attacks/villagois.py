from effects import transformation, buff_stat, resurrection, ressuciter_avec_choix


def coup_de_fourche(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.50)
    reels = cible.prendre_degats(degats)
    return reels

def encouragement(attaquant, cible, equipe):
    for membre in equipe:
        # ne pas compter le villagois
        if membre != attaquant:
            for attaque in membre.cooldowns:
                if membre.cooldowns[attaque] > 0:
                    membre.cooldowns[attaque] = max(0, membre.cooldowns[attaque] - 1)
                    print(f"> Cooldown de l'attaque {attaque} de {membre.nom} réduit à {membre.cooldowns[attaque]}")
    return 0

def transformation_hero(attaquant, cible, equipe):
    
    transformation(attaquant, "Héro", equipe)
    
    return 0

# =========================== héro

    
def frappe_heroique(attaquant, cible, equipe):
    degats = int(attaquant.atk * 1.20)
    reels = cible.prendre_degats(degats)
    return reels

def motivation_du_hero(attaquant, cible, equipe):
    montant_atk = int(attaquant.atk * 0.20)
    montant_def = int(attaquant.defense * 0.20)
    for membre in equipe:
        if membre != attaquant:
            buff_stat(membre, "atk", montant_atk, 2)
            buff_stat(membre, "defense", montant_def, 2)
            # reduire cooldown de 1
            for attaque in membre.cooldowns:    
                if membre.cooldowns[attaque] > 0:
                    membre.cooldowns[attaque] = max(0, membre.cooldowns[attaque] - 1)
                    print(f"> Cooldown de l'attaque {attaque} de {membre.nom} réduit à {membre.cooldowns[attaque]}")
    return 0

def transformation_legende(attaquant, cible, equipe):
    
    transformation(attaquant, "Légende", equipe)
    
    return 0


# =========================== légende
def frappe_legendaire(attaquant, cible, equipe):
    reels = frappe_heroique(attaquant, cible, equipe) 
    if cible.pv / cible.pv_max < 0.20:
        reels += cible.prendre_degats_directs(cible.pv)  
        print(f">{cible.nom} est instantanément tué !")
    return reels


def motivation_legendaire(attaquant, cible, equipe):
    
    motivation_du_hero(attaquant, cible, equipe)
    ressuciter_avec_choix(attaquant, equipe)
    
    return 0
        

def aucun_rival(attaquant, cible, equipe):
    degats = int(cible.pv)
    reels = cible.prendre_degats_directs(degats)
    return reels
