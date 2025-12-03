import random
from models import Item

def generer_loot(items=None):
    rand = random.randint(1, 100)
    cumul = 0
    
    for item_data in items:
        cumul += item_data["chance"]
        if rand <= cumul:
            return Item(item_data)
    return None


def obtenir_loot_apres_combat(equipe, items):

   
    item = generer_loot(items)
    if item:
        print(f"\n Vous avez trouvé : {item.nom} ({item.rarete})")
        print(f"   {item.description}")
        print ("\nChoisissez un héros pour équiper cet item:")
        for idx, hero in enumerate(equipe, 1):
            print(f"   {idx}. {hero.nom}") 
        hero_choisi = input("Choisissez un héros pour équiper cet item : ")
        while True:
            try:
                choix = int(hero_choisi)
                if 1 <= choix <= len(equipe):
                    equipe[choix - 1].equiper_item(item)
                    break
            except ValueError:
                pass
            hero_choisi = input("Choix invalide. Choisissez un héros pour équiper cet item : ")
        return item
    else:
        print("\n Aucun item trouvé après le combat.")
    return None


