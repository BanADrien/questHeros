class Combattant:
    def __init__(self, data, est_heros=True):
        self.nom = data["nom"]
        self.atk = data["atk"]
        self.defense = data["def"]
        self.pv_max = data["pv_max"]
        self.pv = self.pv_max
        self.est_heros = est_heros
        
        if est_heros:
            self.attaques = data["attaques"]
            self.cooldowns = {"special": 0, "ultime": 0}
            
    
    def est_vivant(self):
        return self.pv > 0
    
    def prendre_degats(self, degats):
        reduction = self.defense / (self.defense + 100)
        degats_reels = max(1, int(degats * (1 - reduction)))
        self.pv = max(0, self.pv - degats_reels)
        return degats_reels
    

    def reduire_cooldowns(self):
        for key in self.cooldowns:
            if self.cooldowns[key] > 0:
                self.cooldowns[key] -= 1
                
    def get_fonction_attaque(self, type_attaque):
        import attaques
        nom_fonction = self.attaques[type_attaque]["fonction"]
        return getattr(attaques, nom_fonction)