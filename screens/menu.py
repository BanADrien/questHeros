import pygame
from pixel_style import pixel_style

class Menu:
    def __init__(self, game):
        self.game = game
        self.style = pixel_style
        self.font_title = self.style.font_title
        self.font_button = self.style.font_text
        
        # Charger l'image de fond
        self.background = None
        try:
            import os
            menu_path = "assets/menu.png"
            if os.path.exists(menu_path):
                self.background = pygame.image.load(menu_path)
                self.background = pygame.transform.scale(self.background, (game.WIDTH, game.HEIGHT))
        except Exception as e:
            print(f"Erreur chargement menu.png: {e}")
        
        # Bouton Jouer
        self.btn_jouer = pygame.Rect(
            game.WIDTH // 2 - 150,
            game.HEIGHT // 2 - 80,
            300,
            60
        )
        
        # Bouton Scores
        self.btn_scores = pygame.Rect(
            game.WIDTH // 2 - 150,
            game.HEIGHT // 2 + 10,
            300,
            60
        )
        
        # Bouton Quitter
        self.btn_quitter = pygame.Rect(
            game.WIDTH // 2 - 150,
            game.HEIGHT // 2 + 100,
            300,
            60
        )
        
    def update(self):
        pass
    
    def handle_events(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.btn_jouer.collidepoint(event.pos):
                    # Aller d'abord sur l'écran de choix de pseudo
                    from screens.choix_pseudo import ChoixPseudo
                    self.game.change_screen(ChoixPseudo)
                elif self.btn_scores.collidepoint(event.pos):
                    from screens.scores import Scores
                    self.game.change_screen(Scores)
                elif self.btn_quitter.collidepoint(event.pos):
                    self.game.running = False
    
    def draw(self, screen):
        # Fond d'écran
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((0, 0, 0))
        
        # Overlay semi-transparent pour améliorer la lisibilité
        overlay = pygame.Surface((self.game.WIDTH, self.game.HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Titre avec effet pixel art
        title = self.font_title.render("QUEST HEROES", True, self.style.color_primary)
        title_rect = title.get_rect(center=(self.game.WIDTH // 2, 150))
        # Ombre du titre
        title_shadow = self.font_title.render("QUEST HEROES", True, (50, 50, 50))
        screen.blit(title_shadow, (title_rect.x + 4, title_rect.y + 4))
        screen.blit(title, title_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Boutons avec style pixel art
        self.style.draw_button(screen, self.btn_jouer, "Jouer", self.font_button,
                              self.btn_jouer.collidepoint(mouse_pos),
                              (50, 150, 50) if not self.btn_jouer.collidepoint(mouse_pos) else None)
        
        self.style.draw_button(screen, self.btn_scores, "Scores", self.font_button,
                              self.btn_scores.collidepoint(mouse_pos),
                              (50, 100, 150) if not self.btn_scores.collidepoint(mouse_pos) else None)
        
        self.style.draw_button(screen, self.btn_quitter, "Quitter", self.font_button,
                              self.btn_quitter.collidepoint(mouse_pos),
                              (150, 50, 50) if not self.btn_quitter.collidepoint(mouse_pos) else None)