from db_init import get_db
from datetime import datetime

import os
db = get_db()

def menu_principale_de_combat():
    print("\n" + "="*50)
    print("QUE VEUX TU FAIRE ?")
    print("="*50)
    print("1. Attaquer")
    print("2. Regarder l'équipe")

def menu_demarage():
    print("\n" + "="*50)
    print("MENU PRINCIPAL")
    print("="*50)
    print("1. Nouvelle partie")
    print("2. Initialiser la base de données")
    print("3. Voir les scores")
    print("4. Quitter")


def choix_perso(perso_dispo):
    for id, perso in enumerate(perso_dispo, start=1):
        print(f"{id}. \033[1m{perso['nom']}\033[0m - ATK:{perso['atk']} DEF:{perso['def']} PV:{perso['pv_max']}")
        print(f"{perso['type_perso']} / {perso['description']}\n")

def afficher_details_attaque(hero):
    
    print(f"\nAttaques de {hero.nom}:")
    print("-" * 40)

    # --- Attaque de base ---
    base = hero.attaques["base"]
    print(f"1. {base['nom']}")
    print(f"   Description : {base['description']}")

    # --- Attaque spéciale ---
    special = hero.attaques["special"]
    if hero.cooldowns["special"] == 0:
        print(f"\n2. {special['nom']} (prête)")
    else:
        print(f"\n2. {special['nom']} (cooldown : {hero.cooldowns['special']} tours)")
    print(f"   Description : {special['description']}")

    # --- Attaque ultime ---
    ultimate = hero.attaques["ultime"]
    if hero.cooldowns["ultime"] == 0:
        print(f"\n3. {ultimate['nom']} (prête)")
    else:
        print(f"\n3. {ultimate['nom']} (cooldown : {hero.cooldowns['ultime']} tours)")
    print(f"   Description : {ultimate['description']}")
def afficher_etat_combat(monstre, equipe):
    print("\n" + "="*50)
    print(f"COMBAT CONTRE {monstre.nom.upper()}")
    print("="*50)
    print(f"\n{monstre.nom}: {monstre.pv}/{monstre.pv_max} PV")
    
def afficher_pv_perso(perso):
# ptite interface sympatoche pour le kiff
    pv_maximum = int(perso.pv_max) 
    pv_actuel = int(perso.pv)
    nom = perso.nom
    attaque = perso.atk
    defense = perso.defense
    # Calcul de la barre de vie sur 10 blocs
    ratio = pv_actuel / pv_maximum if pv_maximum > 0 else 0.0
    total_blocs = 10
    blocs_pleins = int(ratio * total_blocs)
    blocs_pleins = max(0, min(total_blocs, blocs_pleins))
    blocs_vides = total_blocs - blocs_pleins

    # Emojis pour la barre
    bloc_plein_emoji = "🟩"
    bloc_vide_emoji = "⬛"
    
    barre_vie = bloc_plein_emoji * blocs_pleins + bloc_vide_emoji * blocs_vides

    # Affichage
    print(f"\n{nom}")
    print(f"[{barre_vie}] {pv_actuel}/{pv_maximum} PV")
    print(f"  ATK : {attaque} / DEF : {defense} / PV MAX : {pv_maximum}")
    print("-"*50)

def afficher_monstre(monstre):
    afficher_pv_perso(monstre)
    input("\nAppuyez sur Entrée pour continuer...")
    
def afficher_equipe(equipe):

    print("\n" + "="*50)
    print("VOTRE ÉQUIPE")
    print("="*50)

    for perso in equipe:
        
        afficher_pv_perso(perso)
    input("\nAppuyez sur Entrée pour continuer...")

def choisir_nom_joueur():
    print("\n" + "="*50)
    print("CHOIX DU NOM DU JOUEUR")
    print("="*50)
    nom_joueur = input("Entrez le nom de votre joueur : ")
    return nom_joueur.strip()

def afficher_scores():
    os.system('cls' if os.name == 'nt' else 'clear')
    scores = list(db.scores.find().sort("victoires", -1).limit(10))
    print("\n" + "="*50)
    print("MEILLEURS SCORES")
    print("="*50)
    
    if not scores:
        print("Aucun score enregistré pour le moment.")
        return
    
    for i, score in enumerate(scores, start=1):
        equipe_str = ', '.join(score['equipe'])
        print(f"joueur: {score['nom_joueur']}")
        print(f"{i}. {score['victoires']}/{score['total_monstres']} victoires")
        print(f"   Équipe: {equipe_str}")
        print(f"   Tours: {score['tours']}")
        print(f"   Date: {score['date'].strftime('%d/%m/%Y %H:%M')}")
        print("-" * 50)


def afficher_intro_combat(monstre):
    print(f"\n\n{'='*50}")
    print(f"UN {monstre.nom.upper()} APPARAÎT!")
    print("="*50)
    input("\nAppuyez sur Entrée pour commencer le combat...")


def afficher_tour(numero_tour):
    print(f"\n{'='*50}")
    print(f"TOUR {numero_tour}")
    print("="*50)


def afficher_resultat_combat(victoire, monstre, victoires, total_monstres):
    if victoire:
        print(f"\nVICTOIRE! Vous avez vaincu le {monstre.nom}!")
        print(f"Score: {victoires}/{total_monstres}")
    else:
        print(f"\nDÉFAITE! Votre équipe a été vaincue par le {monstre.nom}...")
        print(f"Score final: {victoires}/{total_monstres}")
        
