import pygame
from db_init import get_db

class Scores:
    def __init__(self, game):
        self.game = game
        self.font_title = pygame.font.Font(None, 70)
        self.font_text = pygame.font.Font(None, 35)
        self.font_small = pygame.font.Font(None, 28)
        
        # Charger les scores depuis la DB
        self.scores = self.charger_scores()
        
        # Bouton retour
        self.btn_retour = pygame.Rect(
            50,
            game.HEIGHT - 80,
            200,
            50
        )
        
    def charger_scores(self):
        """Charge les 10 meilleurs scores depuis la base de données"""
        db = get_db()
        scores = list(db.scores.find().sort("victoires", -1).limit(10))
        return scores
    
    def update(self):
        pass
    
    def handle_events(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.btn_retour.collidepoint(event.pos):
                    # Retourner au menu
                    from screens.menu import Menu
                    self.game.change_screen(Menu)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # ESC pour retourner au menu
                    from screens.menu import Menu
                    self.game.change_screen(Menu)
    
    def draw(self, screen):
        # Titre
        title = self.font_title.render("Meilleurs Scores", True, (255, 255, 100))
        screen.blit(title, (self.game.WIDTH // 2 - title.get_width() // 2, 40))
        
        # En-têtes du tableau
        y = 140
        headers = ["#", "Joueur", "Victoires", "Tours", "Équipe"]
        x_positions = [100, 200, 450, 650, 800]
        
        for i, header in enumerate(headers):
            text = self.font_text.render(header, True, (200, 200, 200))
            screen.blit(text, (x_positions[i], y))
        
        # Ligne de séparation
        pygame.draw.line(screen, (150, 150, 150), (80, y + 40), (self.game.WIDTH - 80, y + 40), 2)
        
        # Afficher les scores
        y = 200
        if not self.scores:
            no_score_text = self.font_text.render("Aucun score enregistré", True, (150, 150, 150))
            screen.blit(no_score_text, (self.game.WIDTH // 2 - no_score_text.get_width() // 2, y + 100))
        else:
            for idx, score in enumerate(self.scores, 1):
                # Numéro
                num_text = self.font_small.render(f"{idx}.", True, (255, 255, 255))
                screen.blit(num_text, (x_positions[0], y))
                
                # Nom du joueur
                nom = score.get("nom_joueur", "Inconnu")
                nom_text = self.font_small.render(nom[:15], True, (200, 255, 200))
                screen.blit(nom_text, (x_positions[1], y))
                
                # Victoires
                victoires = score.get("victoires", 0)
                total = score.get("total_monstres", 0)
                victoires_text = self.font_small.render(f"{victoires}/{total}", True, (255, 200, 100))
                screen.blit(victoires_text, (x_positions[2], y))
                
                # Tours
                tours = score.get("tours", 0)
                tours_text = self.font_small.render(str(tours), True, (180, 180, 255))
                screen.blit(tours_text, (x_positions[3], y))
                
                # Équipe (noms des héros)
                equipe = score.get("equipe", [])
                equipe_str = ", ".join([h[:8] for h in equipe[:3]])  # Limiter la longueur
                equipe_text = self.font_small.render(equipe_str, True, (200, 200, 200))
                screen.blit(equipe_text, (x_positions[4], y))
                
                y += 45
                
                # Limiter l'affichage pour ne pas dépasser l'écran
                if y > self.game.HEIGHT - 150:
                    break
        
        # Instructions
        instruction = self.font_small.render("Appuyez sur ESC ou cliquez sur Retour", True, (150, 150, 150))
        screen.blit(instruction, (self.game.WIDTH // 2 - instruction.get_width() // 2, self.game.HEIGHT - 120))
        
        # Bouton retour
        mouse_pos = pygame.mouse.get_pos()
        color = (100, 150, 200) if self.btn_retour.collidepoint(mouse_pos) else (50, 100, 150)
        pygame.draw.rect(screen, color, self.btn_retour)
        pygame.draw.rect(screen, (255, 255, 255), self.btn_retour, 3)
        
        text = self.font_text.render("Retour", True, (255, 255, 255))
        screen.blit(text, (self.btn_retour.centerx - text.get_width() // 2, self.btn_retour.centery - text.get_height() // 2))