import pygame
from pixel_style import pixel_style

class ChoixPseudo:
    def __init__(self, game):
        self.game = game
        self.style = pixel_style
        self.font_title = self.style.font_title
        self.font_text = self.style.font_text
        self.font_small = self.style.font_small
        # Centrer l'input box
        self.input_box = pygame.Rect(game.WIDTH // 2 - 300, 340, 600, 60)
        # Centrer le bouton Entrer sous l'input
        self.btn_entrer = pygame.Rect(game.WIDTH // 2 - 100, 430, 200, 60)
        self.pseudo = ""
        self.active = True  # Toujours actif par défaut
        
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

    def handle_events(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Utiliser "Joueur" par défaut si rien n'est saisi
                    pseudo = self.pseudo.strip() if self.pseudo.strip() else "Joueur"
                    self.game.nom_joueur = pseudo
                    from screens.selection_equipe import SelectionEquipe
                    self.game.change_screen(SelectionEquipe)
                elif event.key == pygame.K_BACKSPACE:
                    self.pseudo = self.pseudo[:-1]
                elif len(self.pseudo) < 16 and event.unicode.isprintable():
                    self.pseudo += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_box.collidepoint(event.pos):
                    self.active = True
                elif self.btn_entrer.collidepoint(event.pos):
                    # Clic sur le bouton Entrer
                    pseudo = self.pseudo.strip() if self.pseudo.strip() else "Joueur"
                    self.game.nom_joueur = pseudo
                    from screens.selection_equipe import SelectionEquipe
                    self.game.change_screen(SelectionEquipe)

    def update(self):
        pass

    def draw(self, screen):
        # Fond d'écran
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((15, 25, 40))
        
        # Overlay semi-transparent
        overlay = pygame.Surface((self.game.WIDTH, self.game.HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Titre avec effet pixel art
        title = self.font_title.render("Choisissez votre pseudo", True, self.style.color_primary)
        # Ombre
        title_shadow = self.font_title.render("Choisissez votre pseudo", True, (50, 50, 50))
        screen.blit(title_shadow, (screen.get_width() // 2 - title.get_width() // 2 + 3, 83))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 80))
        
        # Input box avec style pixel art
        self.style.draw_text_input(screen, self.input_box, 
                                   self.pseudo if self.pseudo else "Appuyez pour écrire...", 
                                   self.font_text, 
                                   self.active,
                                   not self.pseudo)
        
        # Bouton Entrer
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.btn_entrer.collidepoint(mouse_pos)
        btn_color = (100, 200, 100) if is_hover else (80, 150, 80)
        border_color = (200, 255, 200) if is_hover else (150, 200, 150)
        
        pygame.draw.rect(screen, btn_color, self.btn_entrer)
        pygame.draw.rect(screen, border_color, self.btn_entrer, 3)
        
        btn_text = self.font_text.render("ENTRER", True, (255, 255, 255))
        text_x = self.btn_entrer.x + (self.btn_entrer.width - btn_text.get_width()) // 2
        text_y = self.btn_entrer.y + (self.btn_entrer.height - btn_text.get_height()) // 2
        screen.blit(btn_text, (text_x, text_y))
