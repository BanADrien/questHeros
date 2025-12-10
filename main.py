from db_init import init_db, get_db
from game import Partie
from db_init import init_db

# Initialiser la DB au démarrage si nécessaire
db = get_db()

if __name__ == "__main__":
    # Lancer directement le jeu en mode GUI
    init_db()
    partie = Partie()
    partie.run()