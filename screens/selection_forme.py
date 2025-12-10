import pygame
from db_init import get_db
from effects import transformation

class SelectionForme:
    def __init__(self, game, attaquant, cible, equipe, formes_disponibles, callback_combat):
        """
        Écran de sélection de forme pour la métamorphose de la druidesse
        
        Args:
            game: Instance du jeu
            attaquant: La druidesse qui se transforme
            cible: Le monstre (pour revenir au combat)
            equipe: L'équipe complète
            formes_disponibles: Liste des formes possibles
            callback_combat: Fonction pour retourner au combat
        """
        self.game = game
        self.attaquant = attaquant
        self.cible = cible
        self.equipe = equipe
        self.formes_disponibles = formes_disponibles
        self.callback_combat = callback_combat
        
        self.font_title = pygame.font.Font(None, 60)
        self.font_text = pygame.font.Font(None, 35)
        self.font_small = pygame.font.Font(None, 28)
        
        # Charger les données complètes des formes
        self.formes_data = []
        db = get_db()
        for forme_nom in formes_disponibles:
            forme_data = db.perso_annexe.find_one({"nom": forme_nom})
            if forme_data:
                self.formes_data.append(forme_data)
        
        # Créer les boutons
        self.boutons_formes = []
        self.creer_boutons_formes()
        
    def creer_boutons_formes(self):
        """Crée les boutons pour chaque forme disponible"""
        self.boutons_formes = []
        
        x_start = 100
        y_start = 200
        largeur = 350
        hauteur = 150
        espacement = 30
        
        for idx, forme in enumerate(self.formes_data):
            ligne = idx // 2
            colonne = idx % 2
            
            x = x_start + colonne * (largeur + espacement)
            y = y_start + ligne * (hauteur + espacement)
            
            btn = {
                "rect": pygame.Rect(x, y, largeur, hauteur),
                "forme": forme,
                "index": idx
            }
            self.boutons_formes.append(btn)
    
    def update(self):
        pass
    
    def handle_events(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in self.boutons_formes:
                    if btn["rect"].collidepoint(event.pos):
                        # Appliquer la transformation
                        self.transformer(btn["forme"]["nom"])
                        return
    
    def transformer(self, forme_choisie):
        """Transforme la druidesse et retourne au combat"""
        _, msg = transformation(self.attaquant, forme_choisie, self.equipe)
        
        # Retourner au combat avec le message
        self.callback_combat(msg)
    
    def draw(self, screen):
        # Titre
        title = self.font_title.render("Choisissez une forme", True, (255, 255, 100))
        screen.blit(title, (self.game.WIDTH // 2 - title.get_width() // 2, 50))
        
        # Info stack
        info = self.font_text.render(
            f"Stacks de transformation : {self.attaquant.stack}",
            True,
            (200, 200, 200)
        )
        screen.blit(info, (self.game.WIDTH // 2 - info.get_width() // 2, 120))
        
        # Dessiner les boutons de formes
        mouse_pos = pygame.mouse.get_pos()
        
        for btn in self.boutons_formes:
            forme = btn["forme"]
            
            # Couleur selon survol
            if btn["rect"].collidepoint(mouse_pos):
                color = (80, 120, 80)
                border_color = (150, 255, 150)
            else:
                color = (60, 80, 60)
                border_color = (100, 180, 100)
            
            pygame.draw.rect(screen, color, btn["rect"])
            pygame.draw.rect(screen, border_color, btn["rect"], 3)
            
            # Nom de la forme
            nom = self.font_text.render(forme["nom"], True, (255, 255, 200))
            screen.blit(nom, (btn["rect"].x + 10, btn["rect"].y + 10))
            
            # Stats
            stats_y = btn["rect"].y + 50
            
            pv = forme.get("pv_max", 0)
            atk = forme.get("atk", 0)
            defense = forme.get("def", 0)
            
            stats = [
                f"PV: {pv}",
                f"ATK: {atk}",
                f"DEF: {defense}"
            ]
            
            for i, stat in enumerate(stats):
                stat_text = self.font_small.render(stat, True, (200, 200, 200))
                screen.blit(stat_text, (btn["rect"].x + 10 + i * 100, stats_y))
            
            # Type
            type_perso = forme.get("type_perso", "N/A")
            type_text = self.font_small.render(f"Type: {type_perso}", True, (180, 180, 180))
            screen.blit(type_text, (btn["rect"].x + 10, stats_y + 35))
        
        # Instructions
        instruction = self.font_small.render(
            "Cliquez sur une forme pour vous transformer",
            True,
            (150, 150, 150)
        )
        screen.blit(instruction, (self.game.WIDTH // 2 - instruction.get_width() // 2, self.game.HEIGHT - 50))