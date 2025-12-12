import pygame
from db_init import get_db
from pixel_style import pixel_style

class SelectionEquipe:
    def __init__(self, game):
        self.game = game
        self.style = pixel_style
        self.font_title = self.style.font_title
        self.font_text = self.style.font_text
        self.font_small = self.style.font_small
        
        # Charger l'image de fond
        self.background = None
        try:
            import os
            menu_path = "assets/menu.png"
            if os.path.exists(menu_path):
                self.background = pygame.image.load(menu_path)
                self.background = pygame.transform.scale(self.background, (1280, 720))
        except Exception as e:
            print(f"Erreur chargement menu.png: {e}")
        self.font_tiny = self.style.font_tiny
        
        # Initialiser la sélection
        self.game.choisir_equipe()
        
        # Scroll pour la liste des héros
        self.scroll_offset = 0
        self.max_visible_rows = 3  # 3 rangées visibles à la fois
        
        # Créer les boutons pour chaque personnage
        self.boutons_persos = []
        self.boutons_selectionnes = []
        self.creer_boutons_personnages()
        
        # Boutons de scroll
        self.btn_scroll_up = pygame.Rect(240, 155, 40, 30)
        self.btn_scroll_down = pygame.Rect(240, 600, 40, 30)
        
        # Popup de détail au survol
        self.popup_perso = None
        self.popup_rect = None
        
        # Bouton Valider (disabled au début) - Plus large pour le texte
        self.btn_valider = pygame.Rect(
            game.WIDTH // 2 - 150,
            game.HEIGHT - 85,
            300,
            60
        )
        
    def creer_boutons_personnages(self):
        """Crée les boutons pour chaque personnage disponible"""
        self.boutons_persos = []
        
        # Layout: 2 colonnes - gauche pour les persos disponibles, droite pour l'équipe
        persos_par_ligne = 2
        largeur_btn = 215
        hauteur_btn = 108
        marge = 16
        start_x = 45
        start_y = 190
        
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
                # Boutons de scroll
                if self.btn_scroll_up.collidepoint(event.pos):
                    self.scroll_offset = max(0, self.scroll_offset - 1)
                    return
                elif self.btn_scroll_down.collidepoint(event.pos):
                    max_rows = (len(self.game.personnages_dispo) + 1) // 2
                    if self.scroll_offset < max_rows - self.max_visible_rows:
                        self.scroll_offset += 1
                    return
                
                # Zone de clipping pour détecter les clics uniquement dans la zone visible
                clip_rect = pygame.Rect(45, 190, 440, 410)
                
                # Vérifier les clics sur les personnages (uniquement ceux visibles)
                if clip_rect.collidepoint(event.pos):
                    for btn in self.boutons_persos:
                        # Vérifier si le personnage est dans la rangée visible
                        row = btn["index"] // 2
                        if row < self.scroll_offset or row >= self.scroll_offset + self.max_visible_rows:
                            continue
                        
                        # Calculer la position ajustée avec le scroll
                        adjusted_y = btn["rect"].y - (self.scroll_offset * 126)
                        adjusted_rect = pygame.Rect(btn["rect"].x, adjusted_y, btn["rect"].width, btn["rect"].height)
                        
                        # Vérifier si le clic est dans le rectangle ajusté
                        if adjusted_rect.collidepoint(event.pos):
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
                    # Afficher l'intro de l'aventure (héros partent à l'aventure)
                    from screens.intro_aventure import IntroAventure
                    self.game.change_screen(lambda g: IntroAventure(g))
    
    def draw(self, screen):
        # Fond d'écran
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((0, 0, 0))
        
        # Overlay semi-transparent pour améliorer la lisibilité
        overlay = pygame.Surface((self.game.WIDTH, self.game.HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Titre avec effet stylé
        title_text = "CHOISISSEZ VOS HEROS"
        title = self.font_title.render(title_text, True, self.style.color_primary)
        title_shadow = self.font_title.render(title_text, True, (40, 40, 40))
        screen.blit(title_shadow, (self.game.WIDTH // 2 - title.get_width() // 2 + 4, 34))
        screen.blit(title, (self.game.WIDTH // 2 - title.get_width() // 2, 30))
        
        # Compteur avec style
        compteur_text = f"Héros sélectionnés : {self.game.heros_choisis} / 3"
        color_compteur = self.style.color_success if self.game.heros_choisis == 3 else self.style.color_primary
        compteur = self.font_text.render(compteur_text, True, color_compteur)
        screen.blit(compteur, (self.game.WIDTH // 2 - compteur.get_width() // 2, 90))
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Afficher les personnages disponibles (à gauche)
        self.dessiner_persos_disponibles(screen, mouse_pos)
        
        # Afficher l'équipe sélectionnée (à droite)
        self.afficher_equipe_selectionnee(screen, mouse_pos)
        
        # Bouton Valider avec style amélioré
        valide = self.game.equipes_pretes()
        if valide:
            btn_color = (50, 150, 50)
            self.style.draw_button(screen, self.btn_valider, "Valider", self.font_text,
                                  self.btn_valider.collidepoint(mouse_pos), btn_color)
        else:
            # Bouton désactivé
            pygame.draw.rect(screen, (60, 60, 60), self.btn_valider)
            pygame.draw.rect(screen, (100, 100, 100), self.btn_valider, 3)
            text = self.font_text.render("Valider", True, (120, 120, 120))
            screen.blit(text, (self.btn_valider.centerx - text.get_width() // 2, self.btn_valider.centery - text.get_height() // 2))
        
        # Afficher le popup de détail au survol
        if self.popup_perso:
            self.afficher_popup_details(screen, self.popup_perso)
    
    def dessiner_persos_disponibles(self, screen, mouse_pos):
        """Affiche les personnages disponibles avec scroll et design amélioré"""
        # Titre de la section
        titre_text = "HEROES DISPONIBLES"
        titre = self.font_text.render(titre_text, True, self.style.color_primary)
        titre_shadow = self.font_text.render(titre_text, True, (30, 30, 30))
        screen.blit(titre_shadow, (47, 147))
        screen.blit(titre, (45, 145))
        
        # Flèches de scroll stylisées
        if self.scroll_offset > 0:
            pygame.draw.polygon(screen, (100, 220, 255), [
                (self.btn_scroll_up.centerx, self.btn_scroll_up.y + 5),
                (self.btn_scroll_up.x + 5, self.btn_scroll_up.bottom - 5),
                (self.btn_scroll_up.right - 5, self.btn_scroll_up.bottom - 5)
            ])
        
        max_rows = (len(self.game.personnages_dispo) + 1) // 2
        if self.scroll_offset < max_rows - self.max_visible_rows:
            pygame.draw.polygon(screen, (100, 220, 255), [
                (self.btn_scroll_down.centerx, self.btn_scroll_down.bottom - 5),
                (self.btn_scroll_down.x + 5, self.btn_scroll_down.y + 5),
                (self.btn_scroll_down.right - 5, self.btn_scroll_down.y + 5)
            ])
        
        self.popup_perso = None

        # Couleurs de bordure par rôle
        role_border_colors = {
            "attaquant": (255, 80, 80),
            "tank": (80, 150, 255),
            "support": (100, 255, 150),
            "polyvalent": (200, 120, 255),
        }

        # Zone de clipping pour le scroll (assez large pour les 2 colonnes)
        clip_rect = pygame.Rect(45, 190, 520, 410)
        screen.set_clip(clip_rect)

        for btn in self.boutons_persos:
            # Calculer position avec scroll
            row = btn["index"] // 2
            if row < self.scroll_offset or row >= self.scroll_offset + self.max_visible_rows:
                continue
                
            adjusted_y = btn["rect"].y - (self.scroll_offset * 126)
            rect = pygame.Rect(btn["rect"].x, adjusted_y, btn["rect"].width, btn["rect"].height)
            is_hovered = rect.collidepoint(mouse_pos) and clip_rect.collidepoint(mouse_pos)

            classe = btn['perso'].get('type_perso', btn['perso'].get('classe', 'N/A'))
            classe_key = str(classe).lower()
            border_color = role_border_colors.get(classe_key, (120, 120, 180))

            # Fond de carte simple
            pygame.draw.rect(screen, (40, 45, 60), rect, border_radius=10)
            
            # Bordure colorée selon la classe (plus épaisse au survol)
            border_width = 4 if is_hovered else 3
            pygame.draw.rect(screen, border_color, rect, border_width, border_radius=10)

            # Barre de titre
            top_bar = pygame.Rect(rect.x + 8, rect.y + 6, rect.width - 16, 26)
            pygame.draw.rect(screen, (50, 55, 70), top_bar, border_radius=6)
            
            # Nom du personnage
            nom_color = (255, 255, 255) if is_hovered else (240, 240, 240)
            nom = self.font_small.render(btn["perso"]["nom"], True, nom_color)
            screen.blit(nom, (top_bar.x + 8, top_bar.y + 5))

            # Stats
            hp = btn['perso'].get('hp') or btn['perso'].get('pv') or btn['perso'].get('pv_max', 0)
            atk = btn['perso'].get('atk') or btn['perso'].get('attaque', 0)
            defense = btn['perso'].get('def') or btn['perso'].get('defense', 0)

            stats_y = rect.y + 40
            hp_text = self.font_tiny.render(f"HP {hp}", True, (255, 120, 120))
            atk_text = self.font_tiny.render(f"ATK {atk}", True, (255, 200, 100))
            def_text = self.font_tiny.render(f"DEF {defense}", True, (120, 200, 255))
            
            screen.blit(hp_text, (rect.x + 12, stats_y))
            screen.blit(atk_text, (rect.x + 80, stats_y))
            screen.blit(def_text, (rect.x + 148, stats_y))
            
            # Classe
            classe_text = self.font_tiny.render(classe, True, (180, 200, 180))
            screen.blit(classe_text, (rect.x + 12, rect.y + 68))
            
            if is_hovered:
                self.popup_perso = btn["perso"]
        
        screen.set_clip(None)
    def afficher_popup_details(self, screen, perso):
        """Affiche un popup avec les détails complets du personnage au survol"""
        # Position du popup : dans l'interstice entre la grille de persos (gauche) et l'équipe sélectionnée (droite)
        popup_w = 380
        popup_h = 280
        popup_x = 470
        popup_y = 180
        
        # Effet d'ombre pour le popup
        shadow_rect = pygame.Rect(popup_x + 6, popup_y + 6, popup_w, popup_h)
        shadow_surf = pygame.Surface((popup_w, popup_h))
        shadow_surf.set_alpha(120)
        shadow_surf.fill((0, 0, 0))
        screen.blit(shadow_surf, (popup_x + 6, popup_y + 6))
        
        # Fond du popup avec style amélioré
        popup_rect = pygame.Rect(popup_x, popup_y, popup_w, popup_h)
        pygame.draw.rect(screen, (25, 35, 55), popup_rect, border_radius=12)
        pygame.draw.rect(screen, (20, 30, 50), popup_rect.inflate(-8, -8), border_radius=10)
        pygame.draw.rect(screen, self.style.color_primary, popup_rect, 4, border_radius=12)
        
        y_offset = popup_y + 15
        
        # Nom avec effet
        nom_text = self.font_text.render(perso["nom"], True, self.style.color_primary)
        nom_shadow = self.font_text.render(perso["nom"], True, (0, 0, 0))
        screen.blit(nom_shadow, (popup_x + 17, y_offset + 2))
        screen.blit(nom_text, (popup_x + 15, y_offset))
        y_offset += 40
        
        # Classe sans icône
        classe = perso.get('type_perso', perso.get('classe', 'N/A'))
        classe_text = self.font_small.render(f"Classe: {classe}", True, (180, 220, 180))
        screen.blit(classe_text, (popup_x + 15, y_offset))
        y_offset += 30
        
        # Stats avec texte simple et couleurs
        hp = perso.get('hp') or perso.get('pv') or perso.get('pv_max', 0)
        atk = perso.get('atk') or perso.get('attaque', 0)
        defense = perso.get('def') or perso.get('defense', 0)
        
        stats_hp = self.font_small.render(f"Vie: {hp}", True, (255, 100, 100))
        stats_atk = self.font_small.render(f"Attaque: {atk}", True, (255, 200, 100))
        stats_def = self.font_small.render(f"Defense: {defense}", True, (100, 200, 255))
        
        screen.blit(stats_hp, (popup_x + 15, y_offset))
        y_offset += 25
        screen.blit(stats_atk, (popup_x + 15, y_offset))
        y_offset += 25
        screen.blit(stats_def, (popup_x + 15, y_offset))
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
        # Positionner le bloc équipe collé au bord droit avec une marge
        x_start = self.game.WIDTH - 360  # 320px de panneau + 40px de marge
        y_start = 190
        self.boutons_selectionnes = []
        
        # Titre de la section aligné avec l'autre titre
        titre_text = "EQUIPE SELECTIONNEE"
        titre = self.font_text.render(titre_text, True, self.style.color_primary)
        titre_shadow = self.font_text.render(titre_text, True, (30, 30, 30))
        titre_x = x_start - 5
        screen.blit(titre_shadow, (titre_x + 2, 147))
        screen.blit(titre, (titre_x, 145))
        
        # Cadre de l'équipe stylisé
        equipe_rect = pygame.Rect(x_start - 10, y_start, 320, 200)
        self.style.draw_panel(screen, equipe_rect, title=None, alpha=190)

        badge_colors = [(255, 215, 0), (120, 200, 255), (180, 255, 180)]

        # Centrer verticalement les héros dans le cadre
        item_height = 48
        item_spacing = 55
        total_height = 0
        if self.game.equipe:
            total_height = item_height + item_spacing * (len(self.game.equipe) - 1)
        start_offset = max(0, (equipe_rect.height - total_height) // 2) if total_height else 0

        for idx, hero in enumerate(self.game.equipe):
            y = y_start + start_offset + idx * item_spacing
            rect = pygame.Rect(x_start + 18, y, 280, 48)
            is_hovered = rect.collidepoint(mouse_pos)

            row_color = (60, 80, 70) if is_hovered else (40, 60, 55)
            pygame.draw.rect(screen, row_color, rect, border_radius=8)
            pygame.draw.rect(screen, (120, 170, 140), rect, 2, border_radius=8)

            # Pastille de rang
            badge_rect = pygame.Rect(rect.x - 16, rect.y + 6, 32, 32)
            pygame.draw.rect(screen, badge_colors[idx % len(badge_colors)], badge_rect, border_radius=6)
            num_text = self.font_small.render(str(idx + 1), True, (20, 20, 20))
            num_rect = num_text.get_rect(center=badge_rect.center)
            screen.blit(num_text, num_rect)

            # Nom du héros
            text = self.font_small.render(hero.nom, True, (210, 240, 210))
            screen.blit(text, (rect.x + 28, rect.y + 10))

            # Indication pour supprimer
            if is_hovered:
                del_text = self.font_tiny.render("clic pour retirer", True, (255, 150, 150))
                screen.blit(del_text, (rect.x + 28, rect.y + 26))

            self.boutons_selectionnes.append({"rect": rect, "index": idx})