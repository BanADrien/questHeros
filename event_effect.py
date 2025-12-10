import item_effects
import events

def verifier_effet_items(equipe_joueurs):
    # Nettoyer les anciens listeners pour éviter les doublons
    # (utile quand on relance un combat)
    events._events["deal_damage"] = []
    events._events["obtention_item"] = []
    events._events["start_turn"] = []
    
    for joueur in equipe_joueurs:
        items = joueur.items

        for item in items:
            effet = item.effet
            if not effet:
                continue

            if "event" in effet:
                nom_event = effet["event"]          
                nom_fonction = effet["fonction"]    
                montant = effet.get("montant", None)
                tours = effet.get("tours", 1)

                # On récupère la fonction dans item_effects
                fonction = getattr(item_effects, nom_fonction, None)
                if fonction is None:
                    print(f"ERREUR: Fonction d'effet d'item '{nom_fonction}' non trouvée dans item_effects.py")
                    continue

                # listener - CORRECTION: adapter les paramètres selon l'événement
                def listener(*args, joueur=joueur, fonction=fonction, item_effet=effet, nom_event=nom_event):
                    event = {}
                    
                    # Adapter les paramètres selon le type d'événement
                    if nom_event == "deal_damage":
                        # args = (attaquant, cible, degats_total, type_attaque, equipe)
                        attaquant = args[0] if len(args) > 0 else None
                        cible = args[1] if len(args) > 1 else None
                        degats_total = args[2] if len(args) > 2 else 0
                        type_attaque = args[3] if len(args) > 3 else None
                        equipe = args[4] if len(args) > 4 else None
                        
                        event = {
                            "attaquant": attaquant,
                            "cible": cible,
                            "degats_total": degats_total,
                            "montant": item_effet.get("montant", None),
                            "tours": item_effet.get("tours", 1),
                            "equipe": equipe,
                            "attaque_type": type_attaque
                        }
                    
                    elif nom_event == "obtention_item":
                        # args = (joueur_equipe, item)
                        joueur_qui_equipe = args[0] if len(args) > 0 else None
                        item_equipe = args[1] if len(args) > 1 else None
                        
                        event = {
                            "attaquant": joueur_qui_equipe,
                            "cible": joueur_qui_equipe,  # La cible c'est le porteur du bouclier
                            "degats_total": 0,
                            "montant": item_effet.get("montant", None),
                            "tours": item_effet.get("tours", 1),
                            "equipe": [joueur_qui_equipe],  # On passe juste le joueur pour simplifier
                            "attaque_type": None,
                            "item": item_equipe
                        }
                    
                    elif nom_event == "start_turn":
                        # args = (personnage)
                        personnage = args[0] if len(args) > 0 else None
                        
                        event = {
                            "attaquant": personnage,
                            "cible": personnage,
                            "degats_total": 0,
                            "montant": item_effet.get("montant", None),
                            "tours": item_effet.get("tours", 1),
                            "equipe": None,
                            "attaque_type": None
                        }
                    
                    # Appeler la fonction avec le joueur et l'event
                    try:
                        fonction(joueur, event)
                    except Exception as e:
                        print(f"ERREUR en appelant {item_effet['fonction']}: {e}")

                # Enregistre le listener
                events.register(nom_event, listener)
