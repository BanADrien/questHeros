import pygame
import os
from pixel_style import pixel_style

class IntroCombat:
    def __init__(self, game, monstre_data):
        self.game = game
        self.monstre_data = monstre_data
        self.style = pixel_style
        self.font_title = self.style.font_title
        self.font_text = self.style.font_text
        
        # Charger l'image du lieu depuis le dossier lieux/
        lieu = monstre_data.get("lieu", "prairie")
        self.background = None
        
        try:
            image_path = os.path.join("assets", "lieux", f"{lieu}.png")
            if os.path.exists(image_path):
                self.background = pygame.image.load(image_path)
                self.background = pygame.transform.scale(self.background, (game.WIDTH, game.HEIGHT))
        except Exception as e:
            print(f"Erreur chargement image du lieu {lieu}: {e}")
        
        # Charger le sprite du monstre depuis le dossier monstres/
        self.monstre_sprite = None
        monstre_nom = monstre_data.get("nom", "").lower()
        
        try:
            sprite_path = os.path.join("assets", "monstres", f"{monstre_nom}.png")
            if os.path.exists(sprite_path):
                self.monstre_sprite = pygame.image.load(sprite_path)
                # Redimensionner le sprite (plus grand)
                sprite_width = 300
                sprite_height = 300
                self.monstre_sprite = pygame.transform.scale(self.monstre_sprite, (sprite_width, sprite_height))
        except Exception as e:
            print(f"Erreur chargement sprite du monstre {monstre_nom}: {e}")
        
        # Timer pour transition automatique (3 secondes)
        self.timer = 180  # 3 secondes à 60 FPS
        
        # Bouton continuer
        self.btn_continuer = pygame.Rect(
            game.WIDTH // 2 - 100,
            game.HEIGHT - 100,
            200,
            50
        )
    
    def update(self):
        # Décompter le timer
        if self.timer > 0:
            self.timer -= 1
            if self.timer == 0:
                self.lancer_combat()
    
    def handle_events(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.btn_continuer.collidepoint(event.pos):
                    self.lancer_combat()
            
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.lancer_combat()
    
    def lancer_combat(self):
        """Lance le combat après l'intro"""
        from screens.combat import Combat
        self.game.initialiser_combat()
        self.game.change_screen(Combat)
    
    def draw(self, screen):
        # Afficher l'image de fond du lieu
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((30, 30, 30))
        
        # Overlay semi-transparent pour améliorer la lisibilité
        overlay = pygame.Surface((self.game.WIDTH, self.game.HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Afficher le sprite du monstre au centre (horizontalement) et plus bas (verticalement)
        if self.monstre_sprite:
            sprite_x = self.game.WIDTH // 2 - 125  # Centré horizontalement
            sprite_y = 350  # Beaucoup plus bas
            screen.blit(self.monstre_sprite, (sprite_x, sprite_y))
        
        # Nom du monstre
        nom_monstre = self.monstre_data.get("nom", "Monstre")
        title = self.font_title.render(f"Un {nom_monstre} approche !", True, (255, 100, 100))
        screen.blit(title, (self.game.WIDTH // 2 - title.get_width() // 2, 100))
        
        # Message d'introduction du lieu + rencontre du monstre avec déterminant personnalisé
        nom_monstre = self.monstre_data.get("nom", "monstre")
        message = self.monstre_data.get("message_intro", "Vous vous préparez au combat...")

        def determiner(monstre_dict):
            # Prend l'article fourni si présent (ex: "une", "la", "le", "un")
            art = monstre_dict.get("article")
            if art:
                return art
            nom = monstre_dict.get("nom", "").lower()
            # Heuristique rapide : noms finissant par e -> "une" sinon "un"
            if nom.endswith("e") or nom.endswith("esse") or nom.endswith("ette"):
                return "une"
            # Cas spéciaux
            if nom in {"mort", "la mort"}:
                return "la"
            return "un"

        article = determiner(self.monstre_data)
        message = f"{message} Et vous y rencontrez {article} {nom_monstre}."
        
        # Wrapper le message sur plusieurs lignes si nécessaire
        words = message.split()
        lines = []
        current_line = ""
        max_width = self.game.WIDTH - 200
        
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if self.font_text.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        
        # Afficher les lignes centrées
        y_offset = 250
        for line in lines:
            text_surface = self.font_text.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (self.game.WIDTH // 2 - text_surface.get_width() // 2, y_offset))
            y_offset += 45
        
        # Bouton continuer
        mouse_pos = pygame.mouse.get_pos()
        color = (100, 150, 100) if self.btn_continuer.collidepoint(mouse_pos) else (70, 120, 70)
        pygame.draw.rect(screen, color, self.btn_continuer)
        pygame.draw.rect(screen, (200, 200, 200), self.btn_continuer, 3)
        
        btn_text = self.font_text.render("Continuer", True, (255, 255, 255))
        screen.blit(btn_text, (self.btn_continuer.centerx - btn_text.get_width() // 2, 
                                self.btn_continuer.centery - btn_text.get_height() // 2))
        
        # Indication timer
        if self.timer > 0:
            timer_text = self.font_text.render(f"Auto: {self.timer // 60 + 1}s", True, (180, 180, 180))
            screen.blit(timer_text, (self.game.WIDTH // 2 - timer_text.get_width() // 2, 
                                     self.btn_continuer.y - 40))
