from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["jeu_video"]

def get_db():
    return db

def init_db():
    personnages = [
        {
            "nom": "Archer",
            "atk": 18,
            "def": 7,
            "pv_max": 90,
            "attaques": {
                "base": {
                    "nom": "Tir rapide",
                    "cooldown": 0,
                    "description": "Un tir précis à 75% de l'attaque",
                    "fonction": "tir_rapide"
                },
                "special": {
                    "nom": "Double tir",
                    "cooldown": 2,
                    "description": "Deux tirs rapides à 40% de l'attaque chacun plus ",
                    "fonction": "double_tir",
                },
                "ultime": {
                    "nom": "Pluie de flèches",
                    "cooldown": 5,
                    "description": "Barrage de flèches 10 flèches infligeant un pourcentage aléatoire entre 20 et 100% de l'attaque chacune",
                    "fonction": "pluie_de_fleches"
                }
            }
        },
        {
            "nom": "Berserker",
            "atk": 23,
            "def": 6,
            "pv_max": 105,
            "attaques": {
                "base": {
                    "nom": "Hache sauvage",
                    "cooldown": 0,
                    "description": "Coup de hache de 70% de l'attaque qui charge la furie de 1",
                    "fonction": "hache_sauvage"
                },
                "special": {
                    "nom": "échauffement",
                    "cooldown": 2,
                    "description": "petite frappe de 20% de l'attaque qui boost l'attaque et charge la furie de 2",
                    "fonction": "echauffement"
                },
                "ultime": {
                    "nom": "déchainement totale",
                    "cooldown": 5,
                    "description": "Utilise toute la furie pour une attaque massive 100% de l'attaque X nombre de charge de furie",
                    "fonction": "dechainement_totale"
                }
            }
        },
        {
            "nom": "Paladin",
            "atk": 14,
            "def": 12,
            "pv_max": 110,
            "attaques": {
                "base": {
                    "nom": "Coup de bouclier",
                    "cooldown": 0,
                    "description": "frappe avec le bouclier avec 50% des pv max en dégats",
                    "fonction": "coup_de_bouclier"
                },
                "special": {
                    "nom": "bénédiction",
                    "cooldown": 2,
                    "description": "Soigne l'équipe de 20% de leurs pv manquant chacun",
                    "fonction": "benediction"
                },
                "ultime": {
                    "nom": "Chatiment",
                    "cooldown": 5,
                    "description": "inflige des dégats équivalent à 100% des pv max du paladin",
                    "fonction": "chatiment"
                }
            }
        },
        {
            "nom": "Mage",
            "atk": 20,
            "def": 5,
            "pv_max": 85,
            "attaques": {
                "base": {
                    "nom": "arcane simple",
                    "cooldown": 0,
                    "description": "inflige 30% de l'attaque et réduit la defense de l'ennemi en fonction de l'attaque du mage",
                    "fonction": "arcane_simple"
                },
                "special": {
                    "nom": "fire ball",
                    "cooldown": 2,
                    "description": "70 % de l'attaque moyens et brûlure",
                    "fonction": "fire_ball"
                },
                "ultime": {
                    "nom": "mal phénoménal",
                    "cooldown": 5,
                    "utilisations_max": 2,
                    "description": "inflige des dégats fixes de 30% des pv manquant de la cible plus 100% de l'attaque du mage",
                    "fonction": "mal_phenomenal"
                }
            }
        }
    ]

    monstres = [
        {"nom": "Gobelin", "atk": 10, "def": 5, "pv_max": 50},
        {"nom": "Loup féroce", "atk": 15, "def": 6, "pv_max": 70},
        {"nom": "Orc", "atk": 20, "def": 8, "pv_max": 120},
        {"nom": "Troll", "atk": 25, "def": 10, "pv_max": 150},
        {"nom": "Dragon", "atk": 35, "def": 20, "pv_max": 300},
    ]

    db.personnages.delete_many({})
    db.monstres.delete_many({})
    db.scores.delete_many({})

    db.personnages.insert_many(personnages)
    db.monstres.insert_many(monstres)

    print(" BDD initialisée")