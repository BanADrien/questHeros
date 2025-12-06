import random
from models import Item


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
    
    if item:
        print(f"\nVous avez obtenu un item : {item.nom} ({item.rarete})")
        print(f"   {item.description}")
        print("\nChoisissez un héros pour équiper cet item:")
        
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
        print("\nAucun item trouvé après le combat.")
    
    return None