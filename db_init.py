from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["jeu_video"]

def get_db():
    return db

def init_db():
    personnages = [
        {
            "nom": "Archer",
            "description": "Tireur d'élite spécialisé dans les attaques à distance.",
            "type_perso": "attaquant",
            "atk": 18,
            "def": 7,
            "pv_max": 90,
            "stack": 0,
            "peut_attaquer": True,
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
            "description": "Guerrier offensif qui utilise de la furie pour augmenter ses dégâts.",
            "type_perso": "attaquant",
            "atk": 23,
            "def": 6,
            "pv_max": 105,
            "stack": 0,
            "peut_attaquer": True,
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
            "description": "Guerrier sacré défensif avec des capacités de soin.",
            "type_perso": "Tank/support",
            "atk": 14,
            "def": 12,
            "pv_max": 110,
            "peut_attaquer": True,
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
            "description": "Utilisateur de magie offensive gagnant 1 atk a chaque sort lancé.",
            "type_perso": "attaquant",
            "atk": 20,
            "def": 5,
            "pv_max": 85,
            "peut_attaquer": True,
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
            "nom": "Hémomancien",
            "description": "Maître du sang utilisant des attaques qui volent la vie et stockent du sang.",
            "type_perso": "tank/attaquant",
            "atk": 15,
            "def": 0,
            "pv_max": 100,
            "peut_attaquer": True,
            "attaques": {
                "base": {
                    "nom": "extraction de sang",
                    "cooldown": 0,
                    "description": "inflige 60% de l'attaque et soigne de 30% des dégats infligés et stock les pv volés en stack de sang",
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
                    "description": "inflige des dégats fixes de 200% des degats et recupère 30% des dégats infligés en pv",
                    "fonction": "siphonage_total"
                }
            }
        },
         {
            "nom": "Assasin",
            "description": "Maître des attaques de status et dégâts lourds.",
            "type_perso": "attaquant",
            "atk": 30,
            "def": 5,
            "pv_max": 70,
            "peut_attaquer": True,
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
                    "description": "inflige 60% de l'attaque et empoisonne pour 3 tours",
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
            "description": "Invocateur de totems avec des capacités de soutien et de dégâts.",
            "type_perso": "support",
            "atk": 15,
            "def": 10,
            "pv_max": 90,
            "peut_attaquer": True,
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
                    "description": "Totem qui boost l'attaque des membres de l'équipe de 20% de leurs attaque pour 2 tours",
                    "fonction": "totem_de_guerre"
                },
                "ultime": {
                    "nom": "Totem de survie",
                    "cooldown": 5,
                    "description": "invoque un Totem qui donne regen 10 et un buff de défense de 10 pendant 3 tours",
                    "fonction": "totem_de_survie"
                }
            }
        },
        {
            "nom": "Villagois",
            "description": "Un simple villageois voulant protéger son village mais on lui remarque un certain potentiel.",
            "type_perso": "support/??",
            "atk": 10,
            "def": 3,
            "pv_max": 65,
            "peut_attaquer": True,
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
                    "cooldown": 10,
                    "description": "???",
                    "fonction": "transformation_hero"
                }
            }
        },
        {
            "nom": "Druidesse",
            "description": "Entité capable de se méthamorphoser en différentes créatures pour s'adapter aux besoins du combat, après 5 méthamorphoses elle se transforme en bêtes mythiques.",
            "type_perso": "polyvalent",
            "atk": 0,
            "def": 0,
            "pv_max": 100,
            "stack": 0,
            "peut_attaquer": True,
            "attaques": {
                "base": {
                    "nom": "métamorphose",
                    "cooldown": 0,
                    "description": "permet de choisir une forme en laquelle se transformer.",
                    "fonction": "methamorphose"
                },
                "special": {
                    "nom": "métamorphose",
                    "cooldown": 0,
                    "description": "permet de choisir une forme en laquelle se transformer.",
                    "fonction": "methamorphose"
                },
                "ultime": {
                    "nom": "métamorphose",
                    "cooldown": 0,
                    "description": "permet de choisir une forme en laquelle se transformer.",
                    "fonction": "methamorphose"
                },
            }
        },
        
    ]
    perso_annexe = [
        {
            "nom": "Héro",
            "description": "Le héros légendaire de la prophétie.",
            "type_perso": "attaquant/support",
            "atk": 35,
            "def": 20,
            "pv_max": 150,
            "peut_attaquer": True,
            "attaques": {
                "base": {
                    "nom": "Frappe Héroïque",
                    "cooldown": 0,
                    "description": "inflige 120% de l'attaque",
                    "fonction": "frappe_heroique"
                },
                "special": {
                    "nom": "motivation du héro",
                    "cooldown": 4,
                    "description": "reduit les cooldowns de 1 pour tous les membres de l'équipe et boost l'attaque et la défense des membres de 20% des stats corespondantes du héro pour 2 tours",
                    "fonction": "motivation_du_hero"
                },
                "ultime": {
                    "nom": "Second éveil",
                    "cooldown": 14,
                    "description": "???",
                    "fonction": "transformation_legende"
                }
            }
        },
        {
            "nom": "Légende",
            "description": "La forme ultime du héros, incarnation de la puissance pure.",
            "type_perso": "attaquant/support",
            "atk": 60,
            "def": 40,
            "pv_max": 250,
            "peut_attaquer": True,
            "attaques": {
                "base": {
                    "nom": "Frappe légendaire",
                    "cooldown": 0,
                    "description": "inflige 120% de l'attaque et tue sous 10% des pv du monstre",
                    "fonction": "frappe_legendaire"
                },
                "special": {
                    "nom": "motivation légendaire",
                    "cooldown": 4,
                    "description": "réssucite un membre de l'équipe, réduit les cooldown des autres membre de 1 ainsi que booster leur attaque et leur défense de 20% des stats corespondantes de la légende pour 2 tours",
                    "fonction": "motivation_legendaire"
                },
                "ultime": {
                    "nom": "Aucun rival",
                    "cooldown": 7,
                    "description": "élimine instantanément le monstre",
                    "fonction": "aucun_rival"
                }
            }
        },
        {
            "nom": "Arraignée géante",
            "description": "bête capable d'empoisonner ou de paralyser ses ennemis.",
            "type_perso": "attaquant",
            "atk": 20,
            "def": 5,
            "pv_max": 100,
            "stack": 0,
            "peut_attaquer": True,
            "attaques": {
                "base": {
                    "nom": "Dard venimeux",
                    "cooldown": 0,
                    "description": "inflige 80% de l'attaque et empoisonne la cible pour 3 tours",
                    "fonction": "dard_venimeux"
                },
                "special": {
                    "nom": "Paralysie",
                    "cooldown": 2,
                    "description": "inflige 20% de l'attaque et paralyse l'ennemi l'empêchant d'attaquer pendant 1 tour",
                    "fonction": "paralysie"
                },
                "ultime": {
                    "nom": "méthamorphose",
                    "cooldown": 4,
                    "description": "se transforme en une autre bête",
                    "fonction": "methamorphose"
                }
            }
        },
        {
            "nom": "Tortue blindée",
            "description": "bête capable de se soigner et de protéger ses alliés.",
            "type_perso": "tank/support",
            "atk": 10,
            "def": 60,
            "pv_max": 100,
            "stack": 0,
            "attaques": {
                "base": {
                    "nom": "auto-guerison",
                    "cooldown": 0,
                    "description": "se regenere 30 pv",
                    "fonction": "auto_guerison"
                },
                "special": {
                    "nom": "carapace partagée",
                    "cooldown": 2,
                    "description": "boost la défense de toute l'équipe de 30 pendant 2 tours",
                    "fonction": "carapace_partagee"
                },
                "ultime": {
                    "nom": "méthamorphose",
                    "cooldown": 4,
                    "description": "se transforme en une autre bête",
                    "fonction": "methamorphose"
                }
            }
        },
        {
            "nom": "Singe savant",
            "description": "bête capable d'augmanter définitivement les stats de ses alliés et de crée un objet aléatoire",
            "type_perso": "support",
            "atk": 20,
            "def": 5,
            "pv_max": 100,
            "stack": 0,
            "attaques": {
                "base": {
                    "nom": "Cours particulier",
                    "cooldown": 0,
                    "description": "donne 5 point d'une stat aléatoire à un allié",
                    "fonction": "cours_particulier"
                },
                "special": {
                    "nom": "invention",
                    "cooldown": 3,
                    "description": "crée un objet aléatoire",
                    "fonction": "invention"
                },
                "ultime": {
                    "nom": "méthamorphose",
                    "cooldown": 4,
                    "description": "se transforme en une autre bête",
                    "fonction": "methamorphose"
                }
            }
        },
        {
            "nom": "Phoenix",
            "description": "bête mythique capable de brûler ainsi que ressusciter et soigner ses alliés.",
            "type_perso": "support/attaquant",
            "atk": 30,
            "def": 10,
            "pv_max": 200,
            "stack": 0,
            "attaques": {
                "base": {
                    "nom": "Feu Sacré",
                    "cooldown": 0,
                    "description": "inflige 100% de l'attaque et brûlure pour 5 tours",
                    "fonction": "feu_sacre"
                },
                "special": {
                    "nom": "feu resurecteur",
                    "cooldown": 4,
                    "description": "ressuscite un allié et appliquer regen 10 aux alliés pour 3 tours",
                    "fonction": "feu_resurecteur"
                },
                "ultime": {
                    "nom": "méthamorphose",
                    "cooldown": 5,
                    "description": "se transforme en une autre bête",
                    "fonction": "methamorphose"
                }
            }
        },
        {
            "nom": "Fenrir",
            "description": "bête mythique infligeant de gros dégats et appliquer saignement et de terrifier l'ennemie.",
            "type_perso": "attaquant",
            "atk": 30,
            "def": 10,
            "pv_max": 200,
            "stack": 0,
            "attaques": {
                "base": {
                    "nom": "déchiquetage",
                    "cooldown": 0,
                    "description": "inflige 150% de l'attaque et applique saignement pour 5 tours",
                    "fonction": "dechiquetage"
                },
                "special": {
                    "nom": "Hurlement",
                    "cooldown": 4,
                    "description": "terrifie l'ennemie ce qui le paralyse pendant 2 tours",
                    "fonction": "hurlement"
                },
                "ultime": {
                    "nom": "méthamorphose",
                    "cooldown": 5,
                    "description": "se transforme en une autre bête",
                    "fonction": "methamorphose"
                }
            }
        },
        {
            "nom": "Golem antique",
            "description": "entité ancienne prennant toute les attaques adverses et capable de se soigner.",
            "type_perso": "tank",
            "atk": 10,
            "def": 100,
            "pv_max": 200,
            "stack": 0,
            "attaques": {
                "base": {
                    "nom": "frappe sismique",
                    "cooldown": 0,
                    "description": "inflige 25% de la défense du golem en dégats et prend forcement le prochain coup de l'ennemie",
                    "fonction": "frappe_sismique"
                },
                "special": {
                    "nom": "Inflexible",
                    "cooldown": 4,
                    "description": "se soigne de 30% de ses pv max et boost sa défense de 30 pour 3 tours",
                    "fonction": "inflexible"
                },
                "ultime": {
                    "nom": "méthamorphose",
                    "cooldown": 5,
                    "description": "se transforme en une autre bête",
                    "fonction": "methamorphose"
                }
            }
        },
    ]
        
    monstres = [
        {"nom": "Gobelin", "atk": 10, "def": 5, "pv_max": 50, "status": [], "peut_attaquer": True, "lieu": "prairie", "article": "un", "message_intro": "Vous pénétrez dans une prairie verdoyante..."},
        {"nom": "Squelette", "atk": 15, "def": 4, "pv_max": 70, "status": [], "peut_attaquer": True, "lieu": "cimetiere", "article": "un", "message_intro": "Un frisson parcourt votre échine en entrant dans ce cimetière..."},
        {"nom": "Loup", "atk": 15, "def": 6, "pv_max": 70, "status": [], "peut_attaquer": True, "lieu": "foret", "article": "un", "message_intro": "Vous vous enfoncez dans une forêt sombre et menaçante..."},
        {"nom": "Orc", "atk": 20, "def": 8, "pv_max": 120, "status": [], "peut_attaquer": True, "lieu": "montagne", "article": "un", "message_intro": "Les montagnes rocheuses s'élèvent devant vous..."},
        {"nom": "Troll", "atk": 25, "def": 10, "pv_max": 150, "status": [], "peut_attaquer": True, "lieu": "montagne", "article": "un", "message_intro": "Vous pataugez dans un marais putride et inhospitalier..."},
        {"nom": "Golem", "atk": 20, "def": 40, "pv_max": 160, "status": [], "peut_attaquer": True, "lieu": "montagne", "article": "un", "message_intro": "L'obscurité de la caverne vous enveloppe..."},
        {"nom": "Dragon", "atk": 35, "def": 20, "pv_max": 300, "status": [], "peut_attaquer": True, "lieu": "volcan", "article": "un", "message_intro": "La chaleur intense du volcan vous assaille..."},
        {"nom": "Demon", "atk": 50, "def": 30, "pv_max": 200, "status": [], "peut_attaquer": True, "lieu": "volcan", "article": "un", "message_intro": "Vous descendez dans les profondeurs infernales..."},
        {"nom": "Ange", "atk": 60, "def": 40, "pv_max": 400, "status": [], "peut_attaquer": True, "lieu": "paradis", "article": "un", "message_intro": "Une lumière divine illumine votre chemin..."},
        {"nom": "La Mort", "atk": 120, "def": 0, "pv_max": 300, "status": [], "peut_attaquer": True, "lieu": "neant", "article": "la", "message_intro": "Le néant vous entoure, la fin est proche..."},
        
        
    ]

    # Items organisés par rareté
    items = {
        "commun": [
            {
                "nom": "Épée rouillée",
                "description": "+3 attaque",
                "stats_bonus": {"atk": 3},
                "effet": None,
                "rarete": "commun"
            },
            {
                "nom": "Vieux bouclier",
                "description": "+3 défense",
                "stats_bonus": {"defense": 3},
                "effet": None,
                "rarete": "commun"
            },
            {
                "nom": "Potion de soin mineure",
                "description": "regen 1 PV par tour",
                "stats_bonus": None,
                "effet": {
                    "event": "start_turn",
                    "fonction": "item_regen",
                    "montant": 1,
                    "tours": 1
                },
                "rarete": "commun"
            }
        ],
        
        "peu_commun": [
            {
                "nom": "Armure de plates",
                "description": "+5 défense, +10 PV max",
                "stats_bonus": {"defense": 5, "pv_max": 10},
                "effet": None,
                "rarete": "peu_commun"
            },
            {
                "nom": "Anneau de vitalité",
                "description": "pv max +15, defense +2",
                "stats_bonus": {"pv_max": 15, "defense": 2},
                "effet": None,
                "rarete": "peu_commun"
            },
            {
                "nom": "Épée en acier",
                "description": "+6 attaque",
                "stats_bonus": {"atk": 6},
                "effet": None,
                "rarete": "peu_commun"
            },
             {
                "nom": "Pierre à aiguiser",
                "description": "+3 attaques, l'attaque de base applique désormais saignement pour 1 tour",
                "stats_bonus": {"atk": 3},
                "effet": {
                    "event": "deal_damage",
                    "fonction": "item_saignement",
                    "tours": 1
                },
                "rarete": "peu_commun"
            },
        ],
        
        "rare": [
            {
                "nom": "Anneau de régénération",
                "description": "defense +1, pv max +5, Régénère 3 PV par tour",
                "stats_bonus": {"defense": 1, "pv_max": 5},
                "effet": {
                    "event": "start_turn",
                    "fonction": "item_regen",
                    "montant": 3,
                    "tours": 1
                },
                "rarete": "rare"
            },
            {
                "nom": "Lame enflammée",
                "description": "+5 attaque, une épée qui brûle les ennemis",
                "stats_bonus": {"atk": 5},
                "effet": {
                    "event": "deal_damage",
                    "fonction": "item_brulure",
                    "tours": 2
                },
                "rarete": "rare"
            },
            {
                "nom": "Bouclier du gardien",
                "description": "+8 défense, +15 PV max, Le porteur devient la cible de toutes les attaques",
                "stats_bonus": {"defense": 8, "pv_max": 15},
                "effet": {
                    "event": "obtention_item",
                    "fonction": "item_prendre_focus",
                },
                "rarete": "rare"
                
            }
        ],
        
        "legendaire": [
            {
                "nom": "Amulette du vampire",
                "description": "+10 attaque, +10 PV max, Vole de la vie à chaque tour",
                "stats_bonus": {"atk": 10, "pv_max": 10},
                "effet": {
                    "event": "deal_damage",
                    "fonction": "item_vol_de_vie",
                    "tours": None
                },
                "rarete": "legendaire"
            },
            {
                "nom": "Couronne du titan",
                "description": "+30 défense, +20 PV max",
                "stats_bonus": {"defense": 30, "pv_max": 20},
                "effet": None,
                "rarete": "legendaire"
            },
            {
                "nom": "Lame de l'infini",
                "description": "+30 attaque, +5 défense, +10 PV max",
                "stats_bonus": {"atk": 30, "defense": 5, "pv_max": 10},
                "effet": None,
                "rarete": "legendaire"
            },
            {
                "nom": "Cape du héro",
                "description": "Transforme le porteur en héros",
                "stats_bonus": None,
                "effet": {
                    "event": "obtention_item",
                    "fonction": "item_transformation_hero",
                },
                "rarete": "legendaire"
            },
            
        ]
    }

        
    db.personnages.delete_many({})
    db.perso_annexe.delete_many({})
    db.monstres.delete_many({})
    db.items.delete_many({})
    

    db.personnages.insert_many(personnages)
    db.perso_annexe.insert_many(perso_annexe)
    db.monstres.insert_many(monstres)
    liste_items = []
    for rarete, items_liste in items.items():
        for it in items_liste:
            it["rarete"] = rarete  # On garde l'information de rareté
            liste_items.append(it)

    db.items.insert_many(liste_items)

    # Charger les scores depuis un fichier JSON local si la collection est vide
    try:
        if db.scores.count_documents({}) == 0:
            import json
            import os
            scores_file = "scores.json"
            if os.path.exists(scores_file):
                with open(scores_file, "r", encoding="utf-8") as f:
                    scores_json = json.load(f)
                if isinstance(scores_json, list) and scores_json:
                    # Limiter à 10 et insérer
                    db.scores.insert_many(scores_json[:10])
    except Exception as e:
        print(f"Import des scores JSON ignoré: {e}")

    print("BDD initialisée")