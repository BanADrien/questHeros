# models.py

class Combattant:
    def __init__(self, data, est_heros=True):
        self.nom = data["nom"]
        self.atk = data["atk"]
        self.defense = data["def"]
        self.pv_max = data["pv_max"]
        self.pv = self.pv_max
        self.stack = 0
        self.est_heros = est_heros
        
        if est_heros:
            self.attaques = data["attaques"]
            self.cooldowns = {
                "base": self.attaques["base"].get("cooldown", 0),
                "special": self.attaques["special"].get("cooldown", 0),
                "ultime": self.attaques["ultime"].get("cooldown", 0)
            }

        self.buffs = []
        self.items = []
        self.status = data.get("status", [])
    
    def est_vivant(self):
        return self.pv > 0
    
    def prendre_degats(self, degats):
        reduction = self.defense / (self.defense + 100)
        degats_reels = max(1, int(degats * (1 - reduction)))
        self.pv = max(0, self.pv - degats_reels)
        return degats_reels
    
    def prendre_degats_directs(self, degats):
        """Dégâts directs sans réduction. Peut être négatif pour soigner"""
        self.pv = max(0, min(self.pv_max, self.pv - degats))
        return abs(degats)
    
    def reduire_cooldowns(self):
        for key in self.cooldowns:
            if self.cooldowns[key] > 0:
                self.cooldowns[key] -= 1
            
    def get_fonction_attaque(self, type_attaque):
        import attaques
        nom_fonction = self.attaques[type_attaque]["fonction"]
        return getattr(attaques, nom_fonction)
    
    def gerer_buffs(self):
        buffs_a_supprimer = []
        for buff in self.buffs:
            buff["tours_restants"] -= 1
            if buff["tours_restants"] <= 0:
                stat = buff["stat"]
                montant = buff["montant"]
                # Retirer l'effet
                if stat == "atk":
                    self.atk -= montant
                elif stat == "defense":
                    self.defense -= montant
                else:
                    setattr(self, stat, getattr(self, stat) - montant)
                buffs_a_supprimer.append(buff)
                print(f"> {self.nom} perd son bonus de {montant} {stat}.")
            else:
                print(f"> {self.nom} a encore {buff['tours_restants']} tours de bonus de {buff['montant']} {buff['stat']}.")
        
        for buff in buffs_a_supprimer:
            self.buffs.remove(buff)
    
    def appliquer_status(self):
        status_a_supprimer = []
        for s in self.status:
            stat = s["stat"]
            montant = s["montant"]
            s["tours_restants"] -= 1

            if stat == "brulure":
                self.pv = max(0, self.pv - montant)
                print(f"> {self.nom} subit {montant} dégâts de brûlure ! (PV : {self.pv}/{self.pv_max})")
            if stat == "poison":
                self.pv = max(0, self.pv - montant)
                print(f"> {self.nom} subit {montant} dégâts de poison ! (PV : {self.pv}/{self.pv_max})")
            if stat == "saignement":
                self.pv = max(0, self.pv - montant)
                print(f"> {self.nom} subit {montant} dégâts de saignement ! (PV : {self.pv}/{self.pv_max})")
            
            if s["tours_restants"] <= 0:
                status_a_supprimer.append(s)

        for s in status_a_supprimer:
            self.status.remove(s)
    
    def equiper_item(self, item):
        """Équipe un item sur le combattant"""
        self.items.append(item)
        
        # Appliquer les bonus de stats permanents
        for stat, val in item.stats_bonus.items():
            if stat == "pv_max":
                self.pv_max += val
                self.pv += val
            elif stat == "atk":
                self.atk += val
            elif stat == "defense":
                self.defense += val
            else:
                setattr(self, stat, getattr(self, stat) + val)
        
        print(f" {self.nom} équipe {item.nom} !")
        if item.stats_bonus:
            bonus_str = ", ".join([f"+{v} {k}" for k, v in item.stats_bonus.items()])
            print(f"   Bonus : {bonus_str}")
    
    def appliquer_effets_items(self):
        
        import effects
        
        for item in self.items:
            if item.effet:
                fonction_nom = item.effet["fonction"]
                fonction = getattr(effects, fonction_nom)
                
                # Appeler la fonction d'effet avec les paramètres
                params = item.effet.copy()
                params.pop("fonction")  # Retirer le nom de fonction des params
                fonction(self, **params)


class Item:
    def __init__(self, data):
        self.nom = data["nom"]
        self.description = data["description"]
        self.stats_bonus = data.get("stats_bonus", {})
        self.effet = data.get("effet", None)
        self.rarete = data.get("rarete", "commun")