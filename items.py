import random
from models import Item
import events

def choisir_rarete(raretes):
    rand = random.randint(1, 100)
    cumul = 0
    
    for rarete, chance in raretes.items():
        cumul += chance
        if rand <= cumul:
            return rarete
    
    return "commun"  


def generer_loot(raretes, items_par_rarete):
    rarete = choisir_rarete(raretes)
    items_disponibles = items_par_rarete.get(rarete, [])

    # Fallback: si aucune entrée pour la rareté tirée, choisir parmi tous les items disponibles
    if not items_disponibles:
        tous_les_items = []
        for lst in items_par_rarete.values():
            tous_les_items.extend(lst)
        if not tous_les_items:
            return None
        item_data = random.choice(tous_les_items)
        return Item(item_data)

    item_data = random.choice(items_disponibles)
    return Item(item_data)


def obtenir_item(equipe, raretes, items_par_rarete):
    item = generer_loot(raretes, items_par_rarete)
    return item


def equiper_item_a_hero(hero, item):
    if hero and item:
        hero.equiper_item(item)
        return True
    return False

    
def test_item_giver(equipe, nom_item, trigger_event=True):
    """Équipe le premier héros avec un item précis et déclenche l'événement d'obtention (optionnel)."""
    from db_init import get_db
    from event_effect import verifier_effet_items
    from effects import transformation

    db = get_db()
    item_data = db.items.find_one({"nom": nom_item}, {"_id": 0})
    if not item_data:
        return None

    item = Item(item_data)
    equipe[0].equiper_item(item)

    # (Re)brancher les effets des items pour le test
    verifier_effet_items(equipe)

    # Déclencher l'événement d'obtention pour tester les effets immédiats (ex: cape -> transformation)
    if trigger_event:
        events.trigger("obtention_item", equipe[0], item, equipe)

    # Fallback: forcer la transformation si cape non appliquée
    if item.nom == "Cape du héro" and equipe[0].nom != "Héro":
        transformation(equipe[0], "Héro", equipe)

    return item