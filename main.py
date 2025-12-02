from db_init import init_db, get_db
from game import Partie
from utils import afficher_scores

db = get_db()

def menu_principal():
    while True:
        print("\n" + "="*50)
        print("MENU PRINCIPAL")
        print("="*50)
        print("1. Nouvelle partie")
        print("2. Initialiser la base de données")
        print("3. Voir les scores")
        print("4. Quitter")
        
        choix = input("\nVotre choix: ")
        
        if choix == "1":
            partie = Partie()
            partie.lancer()
        elif choix == "2":
            init_db()
        elif choix == "3":
            afficher_scores()
        elif choix == "4":
            print("\nCiao!")
            break
        else:
            print("rechoisiss un truc valide")

if __name__ == "__main__":
    menu_principal()