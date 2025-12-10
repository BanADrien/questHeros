import pygame

class Menu:
    def __init__(self, game):
        self.game = game
        self.font_title = pygame.font.Font(None, 80)
        self.font_button = pygame.font.Font(None, 50)
        
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
                    # Lancer la sélection d'équipe
                    from screens.selection_equipe import SelectionEquipe
                    self.game.change_screen(SelectionEquipe)
                    
                elif self.btn_scores.collidepoint(event.pos):
                    # Afficher les scores
                    from screens.scores import Scores
                    self.game.change_screen(Scores)
                    
                elif self.btn_quitter.collidepoint(event.pos):
                    self.game.running = False
    
    def draw(self, screen):
        # Titre
        title = self.font_title.render("MON RPG", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.game.WIDTH // 2, 150))
        screen.blit(title, title_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Bouton Jouer
        color_jouer = (100, 200, 100) if self.btn_jouer.collidepoint(mouse_pos) else (50, 150, 50)
        pygame.draw.rect(screen, color_jouer, self.btn_jouer)
        pygame.draw.rect(screen, (255, 255, 255), self.btn_jouer, 3)
        
        text_jouer = self.font_button.render("Jouer", True, (255, 255, 255))
        text_rect = text_jouer.get_rect(center=self.btn_jouer.center)
        screen.blit(text_jouer, text_rect)
        
        # Bouton Scores
        color_scores = (100, 150, 200) if self.btn_scores.collidepoint(mouse_pos) else (50, 100, 150)
        pygame.draw.rect(screen, color_scores, self.btn_scores)
        pygame.draw.rect(screen, (255, 255, 255), self.btn_scores, 3)
        
        text_scores = self.font_button.render("Scores", True, (255, 255, 255))
        text_rect = text_scores.get_rect(center=self.btn_scores.center)
        screen.blit(text_scores, text_rect)
        
        # Bouton Quitter
        color_quitter = (200, 100, 100) if self.btn_quitter.collidepoint(mouse_pos) else (150, 50, 50)
        pygame.draw.rect(screen, color_quitter, self.btn_quitter)
        pygame.draw.rect(screen, (255, 255, 255), self.btn_quitter, 3)
        
        text_quitter = self.font_button.render("Quitter", True, (255, 255, 255))
        text_rect = text_quitter.get_rect(center=self.btn_quitter.center)
        screen.blit(text_quitter, text_rect)