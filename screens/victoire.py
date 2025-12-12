import pygame
from pixel_style import pixel_style

class Victoire:
    def __init__(self, game):
        self.game = game
        self.style = pixel_style
        self.font_title = self.style.font_title
        self.font_text = self.style.font_text
        self.font_small = self.style.font_small
        
        # Sauvegarder le score
        self.game.sauvegarder_score(self.game.victoires)
        
        # Boutons
        self.btn_menu = pygame.Rect(
            game.WIDTH // 2 - 150,
            game.HEIGHT - 150,
            300,
            60
        )
        
    def update(self):
        pass
    
    def handle_events(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.btn_menu.collidepoint(event.pos):
                    # Retourner au menu
                    from screens.menu import Menu
                    self.game.change_screen(Menu)
    
    def draw(self, screen):
        # Titre
        title = self.font_title.render("VICTOIRE !", True, (255, 255, 100))
        screen.blit(title, (self.game.WIDTH // 2 - title.get_width() // 2, 100))
        
        # Statistiques
        y = 250
        
        stats = [
            f"Monstres vaincus : {self.game.victoires}/{len(self.game.monstres)}",
            f"Tours totaux : {self.game.tour}",
            f"Équipe survivante :"
        ]
        
        for stat in stats:
            text = self.font_text.render(stat, True, (200, 200, 200))
            screen.blit(text, (self.game.WIDTH // 2 - text.get_width() // 2, y))
            y += 50
        
        # Afficher l'équipe
        y += 20
        for hero in self.game.equipe:
            status = "Vivant" if hero.est_vivant() else "K.O."
            color = (100, 255, 100) if hero.est_vivant() else (255, 100, 100)
            text = self.font_small.render(f"  • {hero.nom} - {status} ({hero.pv}/{hero.pv_max} pv)", True, color)
            screen.blit(text, (self.game.WIDTH // 2 - text.get_width() // 2, y))
            y += 40
        
        # Bouton menu
        mouse_pos = pygame.mouse.get_pos()
        color = (100, 200, 100) if self.btn_menu.collidepoint(mouse_pos) else (50, 150, 50)
        pygame.draw.rect(screen, color, self.btn_menu)
        pygame.draw.rect(screen, (255, 255, 255), self.btn_menu, 3)
        
        text = self.font_text.render("Menu principal", True, (255, 255, 255))
        screen.blit(text, (self.btn_menu.centerx - text.get_width() // 2, self.btn_menu.centery - text.get_height() // 2))