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
        self.status = data.get("status", [])
    
    def est_vivant(self):
        return self.pv > 0
    
    def prendre_degats(self, degats):
        reduction = self.defense / (self.defense + 100)
        degats_reels = max(1, int(degats * (1 - reduction)))
        self.pv = max(0, self.pv - degats_reels)
        return degats_reels
    
    def prendre_degats_directs(self, degats):
        self.pv = max(0, self.pv - degats)
        return degats
    

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
                # Retirer l’effet
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
        # Supprimer les buffs expirés
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
            # elif pour rajouter des status si besoin
            
            # Supprimer le status si terminé
            if s["tours_restants"] <= 0:
                status_a_supprimer.append(s)

        for s in status_a_supprimer:
            self.status.remove(s)
