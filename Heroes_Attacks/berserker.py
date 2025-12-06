from effects import buff_stat
def hache_sauvage(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.80)
    reels = cible.prendre_degats(degats)
    attaquant.stack += 1
    print(f"> {attaquant.nom} gagne 1 stack de rage (total : {attaquant.stack})")
    return reels

def echauffement(attaquant, cible, equipe):
    degats = int(attaquant.atk * 0.20)
    reels = cible.prendre_degats(degats)
    attaque = attaquant.atk * 0.25
    buff_stat(attaquant, "atk", int(attaque), 3)
    attaquant.stack += 2
    print(f"> {attaquant.nom} gagne {int(attaque)} points d'attaque (nouvelle ATK : {attaquant.atk}) pendant 2 tours et 2 stacks de rage (total : {attaquant.stack})")
    return reels

def dechainement_totale(attaquant, cible, equipe):
    degats = int(attaquant.atk * (1.00 * attaquant.stack))
    reels = cible.prendre_degats(degats)
    print(f"> {attaquant.nom} utilise {attaquant.stack} stacks de rage pour augmenter les dégâts !")
    attaquant.stack = 0  
    return reels