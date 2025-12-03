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
                    "nom": "Tir précis",
                    "cooldown": 0,
                    "description": "Un tir précis à 75% qui ignore la défense",
                    "fonction": "tir_precis"
                },
                "special": {
                    "nom": "Double tir",
                    "cooldown": 1,
                    "description": "Deux tirs rapides, dégats aléatoire entre 30% et 70% de l'attaque chacun plus ",
                    "fonction": "double_tir",
                },
                "ultime": {
                    "nom": "Pluie de flèches",
                    "cooldown": 4,
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
            "stack": 0,
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
                    "description": "frappe avec le bouclier avec 15% des pv max en dégats",
                    "fonction": "coup_de_bouclier"
                },
                "special": {
                    "nom": "bénédiction",
                    "cooldown": 3,
                    "description": "Soigne l'équipe de 20% de leurs pv manquant chacun",
                    "fonction": "benediction"
                },
                "ultime": {
                    "nom": "Chatiment",
                    "cooldown": 0,
                    "description": "soigne l'équipe de 30% et augmente leurs défense de 50% de la défense du paladin pour 3 tours",
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
                    "cooldown": 0,
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
        {"nom": "Gobelin", "atk": 10, "def": 5, "pv_max": 50, "status": []},
        {"nom": "Squelette", "atk": 15, "def": 4, "pv_max": 70, "status": []},
        {"nom": "Loup féroce", "atk": 15, "def": 6, "pv_max": 70, "status": []},
        {"nom": "Orc", "atk": 20, "def": 8, "pv_max": 120, "status": []},
        {"nom": "Troll", "atk": 25, "def": 10, "pv_max": 150, "status": []},
        {"nom": "Golem", "atk": 20, "def": 40, "pv_max": 160, "status": []},
        {"nom": "Dragon", "atk": 35, "def": 20, "pv_max": 300, "status": []},
        {"nom": "Demon", "atk": 60, "def": 30, "pv_max": 200, "status": []},
        
    ]
    
    items = [
        # ITEMS COMMUNS (50% total)
        {
            "nom": "Épée rouillée",
            "description": "Une vieille épée qui augmente légèrement l'attaque",
            "stats_bonus": {"atk": 3},
            "effet": None,
            "rarete": "commun",
            "chance": 25
        },
        {
            "nom": "Vieux bouclier",
            "description": "Un bouclier usé mais fonctionnel",
            "stats_bonus": {"defense": 3},
            "effet": None,
            "rarete": "commun",
            "chance": 25
        },
        
        # ITEMS PEU COMMUNS (30% total)
        {
            "nom": "Armure de plates",
            "description": "Une solide armure qui augmente la défense",
            "stats_bonus": {"defense": 5, "pv_max": 10},
            "effet": None,
            "rarete": "peu_commun",
            "chance": 15
        },
        {
            "nom": "Anneau de vitalité",
            "description": "Augmente les points de vie maximums",
            "stats_bonus": {"pv_max": 15, "defense": 2},
            "effet": None,
            "rarete": "peu_commun",
            "chance": 15
        },
        
        # ITEMS RARES (15% total)
        {
            "nom": "Anneau de régénération",
            "description": "Régénère 2 PV par tour",
            "stats_bonus": {"defense": 1, "pv_max": 5},
            "effet": {
                "fonction": "effet_regen",
                "montant": 2
            },
            "rarete": "rare",
            "chance": 10
        },
        {
            "nom": "Lame enflammée",
            "description": "Une épée qui brûle les ennemis",
            "stats_bonus": {"atk": 5},
            "effet": {
                "fonction": "brulure",
                "tours": 3
            },
            "rarete": "rare",
            "chance": 5
        },
        
        # ITEMS LÉGENDAIRES (5% total)
        {
            "nom": "Amulette du vampire",
            "description": "Vole de la vie à chaque tour",
            "stats_bonus": {"atk": 4, "pv_max": 10},
            "effet": {
                "fonction": "effet_regen",
                "montant": 5
                
            },
            "rarete": "legendaire",
            "chance": 3
        },
            {
            "nom": "Couronne du titan",
            "description": "Augmente considérablement toutes les stats",
            "stats_bonus": {"atk": 7, "defense": 7, "pv_max": 20},
            "effet": None,
            "rarete": "legendaire",
            "chance": 2
        }
    ]        

    
    db.personnages.delete_many({})
    db.monstres.delete_many({})
    db.items.delete_many({})
    db.scores.delete_many({})

    db.personnages.insert_many(personnages)
    db.monstres.insert_many(monstres)
    db.items.insert_many(items)
    print(" BDD initialisée")