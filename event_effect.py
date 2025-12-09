import item_effects
import events

def verifier_effet_items(equipe_joueurs):

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
                    continue

                # listener
                def listener(*args, joueur=joueur, fonction=fonction, montant=montant, tours=tours):
                    # args = (attaquant, cible, degats_total, type_attaque, equipe)
                    attaquant = args[0]
                    cible = args[1]
                    degats_total = args[2]
                    type_attaque = args[3] if len(args) > 3 else None
                    equipe = args[4] if len(args) > 4 else None

                    event = {
                        "attaquant": attaquant,
                        "cible": cible,
                        "degats_total": degats_total,
                        "montant": montant,
                        "tours": tours,
                        "equipe": equipe,
                        "attaque_type": type_attaque
                    }

                    fonction(joueur, event)

                # Enregistre le listener
                events.register(nom_event, listener)
