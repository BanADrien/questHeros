from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["jeu_video"]

def get_db():
    return db

def init_db():
    personnages = [
        {
            "nom": "Archer",
            "description": "Tireur d'élite spécialisé dans les attaques à distance",
            "type de personnage": "attaquant",
            "atk": 18,
            "def": 7,
            "pv_max": 90,
            "stack": 0,
            "attaques": {
                "base": {
                    "nom": "Tir précis",
                    "cooldown": 0,
                    "description": "Un tir précis à 75% qui ignore la défense, stack 1 flèche",
                    "fonction": "tir_precis"
                },
                "special": {
                    "nom": "Double tir",
                    "cooldown": 1,
                    "description": "Deux tirs rapides, dégats aléatoire entre 30% et 70% de l'attaque chacun plus, stack 2 flèche",
                    "fonction": "double_tir",
                },
                "ultime": {
                    "nom": "Pluie de flèches",
                    "cooldown": 1,
                    "description": "tire autant de flèches que stacké(max15) un pourcentage aléatoire entre 20 et 100% de l'attaque chacune",
                    "fonction": "pluie_de_fleches"
                }
            }
        },
        {
            "nom": "Berserker",
            "description": "Guerrier offensif qui utilise de la furie pour augmenter ses dégats",
            "type de personnage": "attaquant",
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
            "description": "Guerrier sacré défensif avec des capacités de soin",
            "type de personnage": "Tank/support",
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
                    "nom": "prière",
                    "cooldown": 2,
                    "description": "Soigne l'équipe de 10 PV chacun",
                    "fonction": "priere"
                },
                "ultime": {
                    "nom": "bénédiction",
                    "cooldown": 4,
                    "description": "soigne l'équipe de 30% et augmente leurs défense de 50% de la défense du paladin pour 3 tours",
                    "fonction": "benediction"
                }
            }
        },
        {
            "nom": "Mage",
            "description": "Utilisateur de magie offensive gagnant 1 atk a chaque sort lancé",
            "type de personnage": "attaquant",
            "atk": 20,
            "def": 5,
            "pv_max": 85,
            "stack": 0,
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
                    "description": "inflige des dégats fixes de 30% des pv manquant de la cible plus 100% de l'attaque du mage",
                    "fonction": "mal_phenomenal"
                }
            }
        },
        {
            "nom": "hémomancien",
            "description": "Maître du sang utilisant des attaques qui volent la vie et stockent du sang",
            "type de personnage": "tank/attaquant",
            "atk": 15,
            "def": 0,
            "pv_max": 100,
            "stack": 0,
            "attaques": {
                "base": {
                    "nom": "extraction de sang",
                    "cooldown": 0,
                    "description": "inflige 50% de l'attaque et soigne de 50% des dégats infligés et stock les pv volés en stack de sang",
                    "fonction": "extraction_de_sang"
                },
                "special": {
                    "nom": "explosion sanguine",
                    "cooldown": 3,
                    "description": "inflige des degats equivalent à 100% des pv stockés en stack de sang",
                    "fonction": "explosion_sanguine"
                },
                "ultime": {
                    "nom": "siphonage total",
                    "cooldown": 4,
                    "description": "inflige des dégats fixes de 200% des degats et recupère 100% des dégats infligés en pv",
                    "fonction": "siphonage_total"
                }
            }
        },
         {
            "nom": "Assasin",
            "description": "Maître des attaques de status et degats lourds",
            "type de personnage": "attaquant",
            "atk": 30,
            "def": 5,
            "pv_max": 70,
            "stack": 0,
            "attaques": {
                "base": {
                    "nom": "incision",
                    "cooldown": 0,
                    "description": "inflige 50% de l'attaque et inflige saignement pour 3 tours",
                    "fonction": "incision"
                },
                "special": {
                    "nom": "lame toxique",
                    "cooldown": 1,
                    "description": "inflige 40% de l'attaque et empoisonne pour 3 tours",
                    "fonction": "lame_toxique"
                },
                "ultime": {
                    "nom": "assassinat",
                    "cooldown": 5,
                    "description": "inflige des dégats fixes de 200% si la cible à moin de 20% de ses pv elle est éxecutée",
                    "fonction": "assassinat"
                }
            }
        },
         {
            "nom": "Chaman",
            "description": "Invocateur de totems avec des capacités de soutien et de dégâts",
            "type de personnage": "support",
            "atk": 15,
            "def": 10,
            "pv_max": 90,
            "stack": 0,
            "attaques": {
                "base": {
                    "nom": "totem",
                    "cooldown": 0,
                    "description": "¨pose un totem aléatoire qui aura un effet parmis : regen, brulure, poison, ou dégats",
                    "fonction": "totem"
                },
                "special": {
                    "nom": "Totem de guerre",
                    "cooldown": 3,
                    "description": "boost l'attaque des membres de l'équipe de 20% de leurs attaque pour 2 tours",
                    "fonction": "totem_de_guerre"
                },
                "ultime": {
                    "nom": "Totem de survie",
                    "cooldown": 0,
                    "description": "invoque un Totem qui donne regen 10 et un buff de défense de 10 pendant 3 tours",
                    "fonction": "totem_de_survie"
                }
            }
        },
        {
            "nom": "Villagois",
            "atk": 10,
            "def": 3,
            "pv_max": 65,
            "stack": 0,
            "attaques": {
                "base": {
                    "nom": "coup de fourche",
                    "cooldown": 0,
                    "description": "inflige 50% de l'attaque",
                    "fonction": "coup_de_fourche"
                },
                "special": {
                    "nom": "encouragement",
                    "cooldown": 3,
                    "description": "reduit les cooldowns de 1 pour tous les membres de l'équipe",
                    "fonction": "encouragement"
                },
                "ultime": {
                    "nom": "???",
                    "cooldown": 0,
                    "description": "???",
                    "fonction": "transformation_hero"
                }
            }
        },
    ]
    perso_annexe = [
        {
            "nom": "Héro",
            "atk": 35,
            "def": 20,
            "pv_max": 150,
            "stack": 0,
            "attaques": {
                "base": {
                    "nom": "Frappe Héroïque",
                    "cooldown": 0,
                    "description": "inflige 150% de l'attaque",
                    "fonction": "frappe_heroique"
                },
                "special": {
                    "nom": "motivation du héro",
                    "cooldown": 4,
                    "description": "reduit les cooldowns de 1 pour tous les membres de l'équipe et boost l'attque et la défense des membres de 20% des stats corespondantes du héro pour 2 tours",
                    "fonction": "motivation_du_hero"
                },
                "ultime": {
                    "nom": "Second éveil",
                    "cooldown": 0,
                    "description": "???",
                    "fonction": "transformation_legende"
                }
            }
        },
        {
            "nom": "Légende",
            "atk": 60,
            "def": 40,
            "pv_max": 250,
            "stack": 0,
            "attaques": {
                "base": {
                    "nom": "Frappe légendaire",
                    "cooldown": 0,
                    "description": "inflige 150% de l'attaque et tue sous 20% des pv du monstre",
                    "fonction": "frappe_legendaire"
                },
                "special": {
                    "nom": "résurection",
                    "cooldown": 4,
                    "description": "réssucite un membre de l'équipe",
                    "fonction": "resurrection"
                },
                "ultime": {
                    "nom": "Aucun rival",
                    "cooldown": 5,
                    "description": "élimine instantanément le monstre",
                    "fonction": "aucun_rival"
                }
            }
        },
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
        {"nom": "Ange", "atk": 80, "def": 40, "pv_max": 400, "status": []},
        {"nom": "La Mort", "atk": 200, "def": 0, "pv_max": 300, "status": []},
        
        
    ]
        
    raretes = {
        "commun": 40,
        "peu_commun": 30,
        "rare": 20,
        "legendaire": 10
    }

    # Items organisés par rareté
    items = {
        "commun": [
            {
                "nom": "Épée rouillée",
                "description": "Une vieille épée qui augmente légèrement l'attaque",
                "stats_bonus": {"atk": 3},
                "effet": None,
                "rarete": "commun"
            },
            {
                "nom": "Vieux bouclier",
                "description": "Un bouclier usé mais fonctionnel",
                "stats_bonus": {"defense": 3},
                "effet": None,
                "rarete": "commun"
            },
            {
                "nom": "Potion de soin mineure",
                "description": "Restaure quelques PV",
                "stats_bonus": {"pv": 5},
                "effet": None,
                "rarete": "commun"
            }
        ],
        
        "peu_commun": [
            {
                "nom": "Armure de plates",
                "description": "Une solide armure qui augmente la défense",
                "stats_bonus": {"defense": 5, "pv_max": 10},
                "effet": None,
                "rarete": "peu_commun"
            },
            {
                "nom": "Anneau de vitalité",
                "description": "Augmente les points de vie maximums",
                "stats_bonus": {"pv_max": 15, "defense": 2},
                "effet": None,
                "rarete": "peu_commun"
            },
            {
                "nom": "Épée en acier",
                "description": "Une épée de qualité correcte",
                "stats_bonus": {"atk": 6},
                "effet": None,
                "rarete": "peu_commun"
            }
        ],
        
        "rare": [
            {
                "nom": "Anneau de régénération",
                "description": "Régénère 2 PV par tour",
                "stats_bonus": {"defense": 1, "pv_max": 5},
                "effet": {
                    "fonction": "effet_regen",
                    "montant": 2
                },
                "rarete": "rare"
            },
            {
                "nom": "Lame enflammée",
                "description": "Une épée qui brûle les ennemis",
                "stats_bonus": {"atk": 5},
                "effet": {
                    "fonction": "brulure",
                    "tours": 3
                },
                "rarete": "rare"
            },
            {
                "nom": "Bouclier du gardien",
                "description": "Réduit les dégâts reçus",
                "stats_bonus": {"defense": 8, "pv_max": 15},
                "effet": None,
                "rarete": "rare"
            }
        ],
        
        "legendaire": [
            {
                "nom": "Amulette du vampire",
                "description": "Vole de la vie à chaque tour",
                "stats_bonus": {"atk": 4, "pv_max": 10},
                "effet": {
                    "fonction": "effet_regen",
                    "montant": 5
                },
                "rarete": "legendaire"
            },
            {
                "nom": "Couronne du titan",
                "description": "Augmente considérablement toutes les stats",
                "stats_bonus": {"atk": 7, "defense": 7, "pv_max": 20},
                "effet": None,
                "rarete": "legendaire"
            },
            {
                "nom": "Lame de l'infini",
                "description": "Une arme légendaire d'une puissance inouïe",
                "stats_bonus": {"atk": 10, "defense": 3},
                "effet": None,
                "rarete": "legendaire"
            }
        ]
    }

        
    db.personnages.delete_many({})
    db.perso_annexe.delete_many({})
    db.monstres.delete_many({})
    db.items.delete_many({})
    db.raretes.delete_many({})
    db.scores.delete_many({})
    

    db.personnages.insert_many(personnages)
    db.perso_annexe.insert_many(perso_annexe)
    db.monstres.insert_many(monstres)
    liste_items = []
    for rarete, items_liste in items.items():
        for it in items_liste:
            it["rarete"] = rarete  # On garde l'information de rareté
            liste_items.append(it)

    db.items.insert_many(liste_items)
    db.raretes.insert_one(raretes)

    print(" BDD initialisée")