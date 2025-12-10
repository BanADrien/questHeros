import pygame
from items import obtenir_item, equiper_item_a_hero

class SelectionItem:
    def __init__(self, game, item_override=None, retour_combat=False):
        self.game = game
        self.font_title = pygame.font.Font(None, 60)
        self.font_text = pygame.font.Font(None, 30)
        self.font_small = pygame.font.Font(None, 24)
        self.retour_combat = retour_combat
        
        # Générer ou utiliser l'item fourni
        self.item = item_override or obtenir_item(
            self.game.equipe,
            self.game.raretes,
            self.game.items_par_rarete
        )
        
        # Boutons pour chaque héros
        self.boutons_heros = []
        self.creer_boutons_heros()
        
        # Bouton continuer (sans équiper)
        self.btn_continuer = pygame.Rect(
            game.WIDTH // 2 - 100,
            game.HEIGHT - 80,
            200,
            50
        )
        
    def creer_boutons_heros(self):
        """Crée les boutons pour chaque héros"""
        self.boutons_heros = []
        
        x_start = self.game.WIDTH // 2 - 400
        y_start = 300
        
        for idx, hero in enumerate(self.game.equipe):
            btn = {
                "rect": pygame.Rect(x_start + idx * 270, y_start, 250, 100),
                "hero": hero,
                "index": idx
            }
            self.boutons_heros.append(btn)
    
    def equiper_et_continuer(self, hero_index):
        """Équipe l'item au héros et continue"""
        if self.item:
            hero = self.game.equipe[hero_index]
            equiper_item_a_hero(hero, self.item)
            
            # Ré-enregistrer les effets d'items après équiper le nouvel item
            from event_effect import verifier_effet_items
            verifier_effet_items(self.game.equipe)
        
        self.continuer_combat()
    
    def continuer_combat(self):
        """Continue vers le prochain monstre ou retourne au combat en cours"""
        if self.retour_combat:
            # Retourner simplement au combat en cours
            from screens.combat import Combat
            self.game.change_screen(Combat)
            return
        
        monstre = self.game.monstre_suivant()
        
        if monstre is None:
            # Tous les monstres vaincus
            from screens.victoire import Victoire
            self.game.change_screen(Victoire)
        else:
            # Prochain combat
            from screens.combat import Combat
            # Ré-enregistrer les effets d'items pour le nouveau combat
            from event_effect import verifier_effet_items
            verifier_effet_items(self.game.equipe)
            self.game.change_screen(Combat)
    
    def update(self):
        pass
    
    def handle_events(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Vérifier les clics sur les héros
                for btn in self.boutons_heros:
                    if btn["rect"].collidepoint(event.pos):
                        self.equiper_et_continuer(btn["index"])
                        return
                
                # Bouton continuer sans équiper
                if self.btn_continuer.collidepoint(event.pos):
                    self.continuer_combat()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                    self.continuer_combat()
    
    def draw(self, screen):
        # Titre
        if self.item:
            title = self.font_title.render("Item obtenu !", True, (255, 255, 100))
        else:
            title = self.font_title.render("Aucun item...", True, (200, 200, 200))
        
        screen.blit(title, (self.game.WIDTH // 2 - title.get_width() // 2, 50))
        
        if self.item:
            # Nom de l'item
            nom = self.font_title.render(self.item.nom, True, (255, 200, 100))
            screen.blit(nom, (self.game.WIDTH // 2 - nom.get_width() // 2, 120))
            
            # Rareté
            couleurs_rarete = {
                "commun": (200, 200, 200),
                "peu_commun": (100, 255, 100),
                "rare": (100, 100, 255),
                "legendaire": (255, 150, 0)
            }
            rarete_color = couleurs_rarete.get(self.item.rarete, (200, 200, 200))
            rarete = self.font_text.render(f"({self.item.rarete})", True, rarete_color)
            screen.blit(rarete, (self.game.WIDTH // 2 - rarete.get_width() // 2, 180))
            
            # Description
            desc = self.font_small.render(self.item.description, True, (200, 200, 200))
            screen.blit(desc, (self.game.WIDTH // 2 - desc.get_width() // 2, 220))
            
            # Instructions
            instruction = self.font_text.render("Choisissez un héros pour équiper cet item :", True, (255, 255, 255))
            screen.blit(instruction, (self.game.WIDTH // 2 - instruction.get_width() // 2, 260))
        
        # Boutons héros
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.boutons_heros:
            hero = btn["hero"]
            
            # Couleur selon survol
            color = (80, 80, 120) if btn["rect"].collidepoint(mouse_pos) else (60, 60, 100)
            pygame.draw.rect(screen, color, btn["rect"])
            pygame.draw.rect(screen, (200, 200, 200), btn["rect"], 2)
            
            # Nom du héros
            nom = self.font_text.render(hero.nom, True, (255, 255, 255))
            screen.blit(nom, (btn["rect"].x + 10, btn["rect"].y + 10))
            
            # Stats
            stats = self.font_small.render(
                f"pv: {hero.pv}/{hero.pv_max}",
                True,
                (200, 200, 200)
            )
            screen.blit(stats, (btn["rect"].x + 10, btn["rect"].y + 45))
            
            # Items actuels
            if hasattr(hero, 'items') and hero.items:
                items_text = self.font_small.render(f"Items: {len(hero.items)}", True, (180, 180, 180))
                screen.blit(items_text, (btn["rect"].x + 10, btn["rect"].y + 70))
        
        # Bouton continuer
        color = (100, 100, 150) if self.btn_continuer.collidepoint(mouse_pos) else (70, 70, 120)
        pygame.draw.rect(screen, color, self.btn_continuer)
        pygame.draw.rect(screen, (200, 200, 200), self.btn_continuer, 2)
        
        text = self.font_text.render("Continuer sans équiper", True, (255, 255, 255))
        screen.blit(text, (self.btn_continuer.centerx - text.get_width() // 2, self.btn_continuer.centery - text.get_height() // 2))