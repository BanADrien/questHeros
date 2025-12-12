import pygame
import os

class PixelStyle:
    """Style pixel art pour tout le jeu"""
    
    def __init__(self):
        # Polices pixel art (utilise SysFont avec effet pixelisé)
        self.font_title = None
        self.font_large = None
        self.font_text = None
        self.font_small = None
        self.font_tiny = None
        
        # Essayer de charger une police pixel art si disponible
        self.load_fonts()
        
        # Couleurs pixel art fantasy
        self.color_primary = (255, 215, 0)  # Or
        self.color_secondary = (200, 100, 255)  # Violet
        self.color_success = (100, 255, 100)  # Vert
        self.color_danger = (255, 100, 100)  # Rouge
        self.color_text = (255, 255, 255)  # Blanc
        self.color_text_dark = (180, 180, 180)  # Gris clair
        self.color_bg_dark = (20, 20, 40)  # Fond sombre
        self.color_button_normal = (60, 60, 100)
        self.color_button_hover = (80, 80, 150)
        self.color_border = (200, 200, 200)
    
    def load_fonts(self):
        """Charge les polices avec effet pixelisé"""
        pygame.font.init()
        
        # Essayer de charger une police pixel art personnalisée
        custom_font_path = "assets/fonts/pixel.ttf"
        if os.path.exists(custom_font_path):
            try:
                print("Police pixel art personnalisée trouvée !")
                self.font_title = pygame.font.Font(custom_font_path, 56)
                self.font_large = pygame.font.Font(custom_font_path, 42)
                self.font_text = pygame.font.Font(custom_font_path, 28)
                self.font_small = pygame.font.Font(custom_font_path, 22)
                self.font_tiny = pygame.font.Font(custom_font_path, 16)
                return
            except Exception as e:
                print(f"Erreur chargement police personnalisée: {e}")
        
        # Sinon, essayer des polices système avec pixelisation
        print("Utilisation de polices système avec effet pixelisé")
        pixel_fonts = ["Courier New", "Consolas", "Monaco", "monospace"]
        
        for font_name in pixel_fonts:
            try:
                self.font_title = pygame.font.SysFont(font_name, 64, bold=True)
                self.font_large = pygame.font.SysFont(font_name, 48, bold=True)
                self.font_text = pygame.font.SysFont(font_name, 32)
                self.font_small = pygame.font.SysFont(font_name, 24)
                self.font_tiny = pygame.font.SysFont(font_name, 18)
                break
            except:
                continue
        
        # Fallback si aucune police trouvée
        if not self.font_title:
            self.font_title = pygame.font.Font(None, 64)
            self.font_large = pygame.font.Font(None, 48)
            self.font_text = pygame.font.Font(None, 32)
            self.font_small = pygame.font.Font(None, 24)
            self.font_tiny = pygame.font.Font(None, 18)
    
    def draw_button(self, surface, rect, text, font, hovered=False, color_override=None):
        """Dessine un bouton style pixel art"""
        # Couleur selon état
        if color_override:
            bg_color = color_override
        else:
            bg_color = self.color_button_hover if hovered else self.color_button_normal
        
        # Fond du bouton
        pygame.draw.rect(surface, bg_color, rect)
        
        # Bordure pixel art (double bordure)
        pygame.draw.rect(surface, self.color_border, rect, 3)
        pygame.draw.rect(surface, (100, 100, 100), 
                        (rect.x + 2, rect.y + 2, rect.width - 4, rect.height - 4), 1)
        
        # Effet de profondeur (ombre)
        shadow_rect = pygame.Rect(rect.x + 4, rect.y + 4, rect.width, rect.height)
        pygame.draw.rect(surface, (0, 0, 0), shadow_rect, 3)
        
        # Texte centré
        text_surface = font.render(text, True, self.color_text)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)
    
    def draw_panel(self, surface, rect, title=None, alpha=200):
        """Dessine un panneau style pixel art"""
        # Fond du panneau
        panel_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        panel_surface.fill((40, 40, 80, alpha))
        surface.blit(panel_surface, (rect.x, rect.y))
        
        # Bordure pixel art
        pygame.draw.rect(surface, self.color_border, rect, 4)
        pygame.draw.rect(surface, (150, 150, 200), 
                        (rect.x + 3, rect.y + 3, rect.width - 6, rect.height - 6), 2)
        
        # Coins décoratifs
        corner_size = 8
        corners = [
            (rect.x, rect.y),
            (rect.x + rect.width - corner_size, rect.y),
            (rect.x, rect.y + rect.height - corner_size),
            (rect.x + rect.width - corner_size, rect.y + rect.height - corner_size)
        ]
        for corner in corners:
            pygame.draw.rect(surface, self.color_primary, 
                           (corner[0], corner[1], corner_size, corner_size))
        
        # Titre si fourni
        if title:
            title_surface = self.font_text.render(title, True, self.color_primary)
            title_bg = pygame.Rect(rect.centerx - title_surface.get_width() // 2 - 10,
                                  rect.y - 15, title_surface.get_width() + 20, 30)
            pygame.draw.rect(surface, self.color_bg_dark, title_bg)
            pygame.draw.rect(surface, self.color_border, title_bg, 2)
            surface.blit(title_surface, 
                        (rect.centerx - title_surface.get_width() // 2, rect.y - 10))
    
    def draw_text_input(self, surface, rect, text, font, active=False, is_placeholder=False):
        """Dessine un champ de saisie de texte pixel art"""
        # Couleur de la bordure selon l'état
        border_color = (100, 200, 255) if active else (80, 100, 150)
        
        # Fond du champ
        pygame.draw.rect(surface, (30, 40, 60), rect)
        
        # Bordure avec effet glow si actif
        pygame.draw.rect(surface, border_color, rect, 4)
        
        if active:
            # Double bordure pour effet de focus
            glow_rect = rect.inflate(6, 6)
            pygame.draw.rect(surface, border_color, glow_rect, 2)
        
        # Texte
        text_color = (120, 120, 120) if is_placeholder else (255, 255, 255)
        txt_surface = font.render(text, True, text_color)
        surface.blit(txt_surface, (rect.x + 15, rect.y + rect.height // 2 - txt_surface.get_height() // 2))
    
    def draw_hp_bar(self, surface, x, y, width, height, current, maximum):
        """Dessine une barre de vie pixel art"""
        # Fond
        pygame.draw.rect(surface, (50, 50, 50), (x, y, width, height))
        
        # Barre de vie
        hp_percent = max(0, min(1, current / maximum if maximum > 0 else 0))
        hp_width = int(width * hp_percent)
        
        # Couleur selon le pourcentage
        if hp_percent > 0.6:
            hp_color = (100, 255, 100)
        elif hp_percent > 0.3:
            hp_color = (255, 200, 100)
        else:
            hp_color = (255, 100, 100)
        
        pygame.draw.rect(surface, hp_color, (x, y, hp_width, height))
        
        # Bordure
        pygame.draw.rect(surface, self.color_border, (x, y, width, height), 2)
        
        # Texte HP
        hp_text = self.font_tiny.render(f"{current}/{maximum}", True, self.color_text)
        surface.blit(hp_text, (x + width + 5, y + height // 2 - hp_text.get_height() // 2))

# Instance globale du style
pixel_style = PixelStyle()
