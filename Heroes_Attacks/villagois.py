from effects import transformation, buff_stat, resurrection


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
    degats = int(attaquant.atk * 1.50)
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
    # choisir un membre mort a ressuciter
    membres_morts = [membre for membre in equipe if not membre.est_vivant()]
    if membres_morts.len() == 1:
        membre_a_ressusciter = membres_morts[0]
        resurrection(membre_a_ressusciter)
        print(f"> {membre_a_ressusciter.nom} a été ressuscité")
        return 0
    elif membres_morts.len() > 1:
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
        

def aucun_rival(attaquant, cible, equipe):
    degats = int(cible.pv)
    reels = cible.prendre_degats_directs(degats)
    return reels
