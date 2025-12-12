import pygame
from pixel_style import pixel_style

class ChoixPseudo:
    def __init__(self, game):
        self.game = game
        self.style = pixel_style
        self.font_title = self.style.font_title
        self.font_text = self.style.font_text
        self.font_small = self.style.font_small
        self.input_box = pygame.Rect(340, 340, 600, 60)
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
        
        # Indication
        info = self.font_small.render("Appuyez sur Entrée pour continuer (défaut: Joueur)", True, (150, 200, 150))
        screen.blit(info, (self.input_box.x, self.input_box.y + 70))
