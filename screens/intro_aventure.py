import pygame
from pixel_style import pixel_style

class IntroAventure:
    """Écran d'introduction montrant les héros qui partent à l'aventure"""
    
    def __init__(self, game):
        self.game = game
        self.style = pixel_style
        self.font_titre = self.style.font_title
        self.font_texte = self.style.font_text
        self.font_small = self.style.font_small
        
        # S'assurer que les monstres sont chargés
        if not self.game.monstres:
            self.game.charger_monstres()
        
        # Charger l'image de fond d'intro
        self.background = None
        try:
            import os
            intro_path = "assets/intro.png"
            if os.path.exists(intro_path):
                self.background = pygame.image.load(intro_path)
                self.background = pygame.transform.scale(self.background, (1280, 720))
        except Exception as e:
            print(f"Erreur chargement intro.png: {e}")
        
        # Timer pour passer automatiquement à l'écran suivant
        self.timer = 240
        
        # Noms des héros
        self.equipe_noms = [hero.nom for hero in self.game.equipe]
    
    def draw(self, screen):
        """Affiche l'écran d'introduction épuré"""
        # Fond d'écran
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((20, 30, 50))
        
        # Overlay semi-transparent
        overlay = pygame.Surface((self.game.WIDTH, self.game.HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Petit message en haut
        header_surface = self.font_small.render("L'aventure commence...", True, (180, 180, 180))
        header_rect = header_surface.get_rect(center=(640, 100))
        screen.blit(header_surface, header_rect)
        
        # Construire la phrase avec les noms des héros
        if len(self.equipe_noms) == 1:
            phrase = f"{self.equipe_noms[0]} part à l'aventure"
        elif len(self.equipe_noms) == 2:
            phrase = f"{self.equipe_noms[0]} et {self.equipe_noms[1]} partent à l'aventure"
        else:
            phrase = f"{', '.join(self.equipe_noms[:-1])} et {self.equipe_noms[-1]} partent à l'aventure"
        
        # Afficher la phrase
        phrase_surface = self.font_texte.render(phrase, True, (255, 215, 0))
        phrase_rect = phrase_surface.get_rect(center=(640, 350))
        screen.blit(phrase_surface, phrase_rect)
        
        # Message discret en bas
        hint_surface = self.font_small.render("Appuyez sur une touche pour continuer", True, (120, 120, 120))
        hint_rect = hint_surface.get_rect(center=(640, 670))
        screen.blit(hint_surface, hint_rect)
    
    def handle_events(self, event_list):
        """Gère les événements de l'écran"""
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.passer_au_combat()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Permettre de cliquer n'importe où pour passer
                self.passer_au_combat()
    
    def update(self):
        """Met à jour l'état de l'écran (timer)"""
        if self.timer > 0:
            self.timer -= 1
            if self.timer == 0:
                self.passer_au_combat()
    
    def passer_au_combat(self):
        """Passe à l'écran d'introduction du premier monstre"""
        from screens.intro_combat import IntroCombat
        
        # Récupérer les infos du premier monstre
        monstre = self.game.obtenir_monstre_actuel()
        
        if monstre is None:
            # Si pas de monstre, retourner au menu
            from screens.menu import Menu
            self.game.change_screen(Menu)
            return
        
        # Construire le dictionnaire monstre_dict
        if hasattr(monstre, '_raw_data'):
            monstre_dict = monstre._raw_data
        else:
            monstre_dict = {
                "nom": monstre.nom,
                "lieu": getattr(monstre, "lieu", "menu"),
                "message_intro": getattr(monstre, "message_intro", "Un monstre apparaît !")
            }
        
        self.game.change_screen(lambda g: IntroCombat(g, monstre_dict))
