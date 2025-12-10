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
    
    if not items_disponibles:
        return None
    
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

    
def test_item_giver(equipe, nom_item):
    from db_init import get_db
    db = get_db()
    item_data = db.items.find_one({"nom": nom_item}, {"_id": 0}) 
    if item_data:
        item = Item(item_data)
        equipe[0].equiper_item(item)
        return item
    return None