import pygame
from db_init import get_db

class SelectionEquipe:
    def __init__(self, game):
        self.game = game
        self.font_title = pygame.font.Font(None, 60)
        self.font_text = pygame.font.Font(None, 30)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 20)
        
        # Initialiser la sélection
        self.game.choisir_equipe()
        
        # Créer les boutons pour chaque personnage
        self.boutons_persos = []
        self.boutons_selectionnes = []
        self.creer_boutons_personnages()
        
        # Popup de détail au survol
        self.popup_perso = None
        self.popup_rect = None
        
        # Bouton valider (disabled au début)
        self.btn_valider = pygame.Rect(
            game.WIDTH // 2 - 100,
            game.HEIGHT - 80,
            200,
            50
        )
        
    def creer_boutons_personnages(self):
        """Crée les boutons pour chaque personnage disponible"""
        self.boutons_persos = []
        
        # Layout: 2 colonnes - gauche pour les persos disponibles, droite pour l'équipe
        persos_par_ligne = 2
        largeur_btn = 200
        hauteur_btn = 110
        marge = 15
        start_x = 40
        start_y = 150
        
        for idx, perso in enumerate(self.game.personnages_dispo):
            ligne = idx // persos_par_ligne
            colonne = idx % persos_par_ligne
            
            x = start_x + colonne * (largeur_btn + marge)
            y = start_y + ligne * (hauteur_btn + marge)
            
            btn = {
                "rect": pygame.Rect(x, y, largeur_btn, hauteur_btn),
                "perso": perso,
                "index": idx
            }
            self.boutons_persos.append(btn)
    
    def update(self):
        pass
    
    def handle_events(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Vérifier les clics sur les personnages
                for btn in self.boutons_persos:
                    if btn["rect"].collidepoint(event.pos):
                        # Sélectionner ce héros
                        if self.game.selectionner_hero(btn["index"]):
                            # Recréer les boutons (un perso a été retiré)
                            self.creer_boutons_personnages()
                        break

                # Vérifier les clics sur l'équipe (désélection)
                for btn_sel in self.boutons_selectionnes:
                    if btn_sel["rect"].collidepoint(event.pos):
                        if self.game.deselectionner_hero(btn_sel["index"]):
                            self.creer_boutons_personnages()
                        break
                
                # Vérifier le bouton valider
                if self.btn_valider.collidepoint(event.pos) and self.game.equipes_pretes():
                    # Lancer le combat
                    from screens.combat import Combat
                    self.game.initialiser_combat()
                    self.game.change_screen(Combat)
    
    def draw(self, screen):
        # Titre
        title = self.font_title.render("Choisissez 3 héros", True, (255, 255, 255))
        screen.blit(title, (self.game.WIDTH // 2 - title.get_width() // 2, 30))
        
        # Compteur
        compteur_text = self.font_text.render(
            f"Héros choisis : {self.game.heros_choisis} / 3",
            True,
            (200, 200, 200)
        )
        screen.blit(compteur_text, (self.game.WIDTH // 2 - compteur_text.get_width() // 2, 90))
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Afficher les personnages disponibles (à gauche)
        self.dessiner_persos_disponibles(screen, mouse_pos)
        
        # Afficher l'équipe sélectionnée (à droite)
        self.afficher_equipe_selectionnee(screen, mouse_pos)
        
        # Bouton Valider
        valide = self.game.equipes_pretes()
        if valide:
            color = (100, 200, 100) if self.btn_valider.collidepoint(mouse_pos) else (50, 150, 50)
        else:
            color = (80, 80, 80)
        
        pygame.draw.rect(screen, color, self.btn_valider)
        pygame.draw.rect(screen, (255, 255, 255), self.btn_valider, 3)
        
        text = self.font_text.render("Valider", True, (255, 255, 255))
        screen.blit(text, (self.btn_valider.centerx - text.get_width() // 2, self.btn_valider.centery - text.get_height() // 2))
        
        # Afficher le popup de détail au survol
        if self.popup_perso:
            self.afficher_popup_details(screen, self.popup_perso)
    
    def dessiner_persos_disponibles(self, screen, mouse_pos):
        """Affiche les personnages disponibles avec un layout 2 colonnes"""
        # Titre de la section
        titre = self.font_text.render("Personnages disponibles :", True, (200, 200, 255))
        screen.blit(titre, (40, 115))
        
        self.popup_perso = None
        
        for btn in self.boutons_persos:
            # Couleur selon survol
            is_hovered = btn["rect"].collidepoint(mouse_pos)
            color = (80, 100, 120) if is_hovered else (50, 70, 90)
            pygame.draw.rect(screen, color, btn["rect"])
            pygame.draw.rect(screen, (150, 150, 200), btn["rect"], 2)
            
            # Nom du personnage
            nom = self.font_text.render(btn["perso"]["nom"], True, (255, 255, 255))
            screen.blit(nom, (btn["rect"].x + 8, btn["rect"].y + 8))
            
            # Stats compacts
            hp = btn['perso'].get('hp') or btn['perso'].get('pv') or btn['perso'].get('pv_max', 0)
            atk = btn['perso'].get('atk') or btn['perso'].get('attaque', 0)
            defense = btn['perso'].get('def') or btn['perso'].get('defense', 0)
            
            stats_text = self.font_tiny.render(
                f"HP:{hp} ATK:{atk} DEF:{defense}",
                True,
                (180, 180, 180)
            )
            screen.blit(stats_text, (btn["rect"].x + 8, btn["rect"].y + 35))
            
            # Classe / type
            classe_text = self.font_tiny.render(
                f"{btn['perso'].get('type_perso', btn['perso'].get('classe', 'N/A'))}",
                True,
                (150, 200, 150)
            )
            screen.blit(classe_text, (btn["rect"].x + 8, btn["rect"].y + 55))
            
            # Hover -> afficher popup avec description
            if is_hovered:
                self.popup_perso = btn["perso"]
    
    def afficher_popup_details(self, screen, perso):
        """Affiche un popup avec les détails complets du personnage au survol"""
        # Position du popup : dans l'interstice entre la grille de persos (gauche) et l'équipe sélectionnée (droite)
        popup_w = 360
        popup_h = 260
        popup_x = 480
        popup_y = 150
        
        # Fond du popup
        surface = pygame.Surface((popup_w, popup_h))
        surface.fill((30, 40, 50))
        screen.blit(surface, (popup_x, popup_y))
        
        # Bordure
        pygame.draw.rect(screen, (150, 200, 255), (popup_x, popup_y, popup_w, popup_h), 3)
        
        y_offset = popup_y + 10
        
        # Nom
        nom_text = self.font_text.render(perso["nom"], True, (255, 255, 100))
        screen.blit(nom_text, (popup_x + 10, y_offset))
        y_offset += 35
        
        # Classe
        classe_text = self.font_small.render(f"Classe: {perso.get('type_perso', perso.get('classe', 'N/A'))}", True, (150, 200, 150))
        screen.blit(classe_text, (popup_x + 10, y_offset))
        y_offset += 25
        
        # Stats
        hp = perso.get('hp') or perso.get('pv') or perso.get('pv_max', 0)
        atk = perso.get('atk') or perso.get('attaque', 0)
        defense = perso.get('def') or perso.get('defense', 0)
        
        stats_text = self.font_small.render(f"HP: {hp} | ATK: {atk} | DEF: {defense}", True, (200, 200, 200))
        screen.blit(stats_text, (popup_x + 10, y_offset))
        y_offset += 30
        
        # Description
        def wrap_text(text, font, max_width):
            words = text.split()
            lines = []
            current = ""
            for w in words:
                tentative = f"{current} {w}".strip()
                if font.size(tentative)[0] <= max_width:
                    current = tentative
                else:
                    if current:
                        lines.append(current)
                    current = w
            if current:
                lines.append(current)
            return lines
        
        desc = perso.get("description", "") or "Pas de description."
        desc_lines = wrap_text(desc, self.font_small, popup_w - 20)[:3]
        
        desc_label = self.font_small.render("Description :", True, (200, 200, 100))
        screen.blit(desc_label, (popup_x + 10, y_offset))
        y_offset += 22
        
        for line in desc_lines:
            text_surface = self.font_small.render(line, True, (200, 200, 200))
            screen.blit(text_surface, (popup_x + 10, y_offset))
            y_offset += 20
        
        y_offset += 5
        
        # Pas d'affichage des attaques ici : les descriptions sont visibles lors du choix d'attaque en combat
    
    def afficher_equipe_selectionnee(self, screen, mouse_pos):
        """Affiche l'équipe sélectionnée sur la droite"""
        x_start = self.game.WIDTH - 320
        y_start = 150
        self.boutons_selectionnes = []
        
        # Titre de la section
        title = self.font_text.render("Équipe sélectionnée :", True, (255, 255, 100))
        screen.blit(title, (x_start, y_start - 40))
        
        # Cadre de l'équipe
        equipe_rect = pygame.Rect(x_start - 10, y_start - 10, 310, 160)
        pygame.draw.rect(screen, (40, 40, 60), equipe_rect)
        pygame.draw.rect(screen, (150, 150, 200), equipe_rect, 2)
        
        for idx, hero in enumerate(self.game.equipe):
            y = y_start + idx * 45
            rect = pygame.Rect(x_start, y, 280, 38)
            
            is_hovered = rect.collidepoint(mouse_pos)
            color = (80, 100, 80) if is_hovered else (50, 70, 50)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (120, 180, 120), rect, 2)
            
            text = self.font_small.render(f"{idx+1}. {hero.nom}", True, (200, 255, 200))
            screen.blit(text, (rect.x + 10, rect.y + 8))
            
            # Indication pour supprimer
            if is_hovered:
                del_text = self.font_tiny.render("[Clic pour retirer]", True, (255, 100, 100))
                screen.blit(del_text, (rect.x + 10, rect.y + 20))
            
            self.boutons_selectionnes.append({"rect": rect, "index": idx})