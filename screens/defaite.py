import pygame
from pixel_style import pixel_style

class Defaite:
    def __init__(self, game):
        self.game = game
        self.style = pixel_style
        self.font_title = self.style.font_title
        self.font_text = self.style.font_text
        self.font_small = self.style.font_small
        
        # Sauvegarder le score
        self.game.sauvegarder_score(self.game.victoires)
        
        # Boutons
        self.btn_recommencer = pygame.Rect(
            game.WIDTH // 2 - 150,
            game.HEIGHT - 200,
            300,
            60
        )
        
        self.btn_menu = pygame.Rect(
            game.WIDTH // 2 - 150,
            game.HEIGHT - 120,
            300,
            60
        )
        
    def update(self):
        pass
    
    def handle_events(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.btn_recommencer.collidepoint(event.pos):
                    # Recommencer une partie
                    from screens.selection_equipe import SelectionEquipe
                    self.game.change_screen(SelectionEquipe)
                    
                elif self.btn_menu.collidepoint(event.pos):
                    # Retourner au menu
                    from screens.menu import Menu
                    self.game.change_screen(Menu)
    
    def draw(self, screen):
        # Titre
        title = self.font_title.render("DÉFAITE", True, (255, 100, 100))
        screen.blit(title, (self.game.WIDTH // 2 - title.get_width() // 2, 100))
        
        # Message
        message = self.font_text.render("Votre équipe a été vaincue...", True, (200, 200, 200))
        screen.blit(message, (self.game.WIDTH // 2 - message.get_width() // 2, 200))
        
        # Statistiques
        y = 280
        
        stats = [
            f"Monstres vaincus : {self.game.victoires}/{len(self.game.monstres)}",
            f"Tours survécus : {self.game.tour}",
        ]
        
        for stat in stats:
            text = self.font_small.render(stat, True, (180, 180, 180))
            screen.blit(text, (self.game.WIDTH // 2 - text.get_width() // 2, y))
            y += 40
        
        # Bouton recommencer
        mouse_pos = pygame.mouse.get_pos()
        color = (100, 150, 255) if self.btn_recommencer.collidepoint(mouse_pos) else (50, 100, 200)
        pygame.draw.rect(screen, color, self.btn_recommencer)
        pygame.draw.rect(screen, (255, 255, 255), self.btn_recommencer, 3)
        
        text = self.font_text.render("Recommencer", True, (255, 255, 255))
        screen.blit(text, (self.btn_recommencer.centerx - text.get_width() // 2, self.btn_recommencer.centery - text.get_height() // 2))
        
        # Bouton menu
        color = (100, 100, 100) if self.btn_menu.collidepoint(mouse_pos) else (70, 70, 70)
        pygame.draw.rect(screen, color, self.btn_menu)
        pygame.draw.rect(screen, (255, 255, 255), self.btn_menu, 3)
        
        text = self.font_text.render("Menu principal", True, (255, 255, 255))
        screen.blit(text, (self.btn_menu.centerx - text.get_width() // 2, self.btn_menu.centery - text.get_height() // 2))