import pygame
from db_init import get_db
from pixel_style import pixel_style
import os
import unicodedata

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
                self.background = pygame.transform.scale(self.background, (game.WIDTH, game.HEIGHT))
        except Exception as e:
            print(f"Erreur chargement menu.png: {e}")
        self.font_tiny = self.style.font_tiny
        
        # Initialiser la sélection
        self.game.choisir_equipe()
        
        # Scroll pour la liste des héros
        self.scroll_offset = 0

        # Cache images (icônes et splashs) et paramètres de grille
        self._icon_cache = {}
        self._splash_cache = {}
        self.icon_size = 96
        self.icon_padding = 18
        # Hauteur de rangée pour le scroll (icône + padding)
        self.row_height = self.icon_size + self.icon_padding  # utile pour le scroll
        # Marge gauche de la grille (légèrement décalée à droite)
        self.grid_left = 110
        
        # Créer les boutons pour chaque personnage
        self.boutons_persos = []
        self.boutons_selectionnes = []
        self.creer_boutons_personnages()
        
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

        
        
    def _slug(self, s: str) -> str:
        s = s.strip().lower()
        s = ''.join(
            c for c in unicodedata.normalize('NFD', s)
            if unicodedata.category(c) != 'Mn'
        )
        allowed = "abcdefghijklmnopqrstuvwxyz0123456789-_ "
        s = ''.join(ch if ch in allowed else ' ' for ch in s)
        s = '-'.join(filter(None, s.replace('_', ' ').split()))
        return s

    def _nom_to_asset_key(self, nom: str) -> str:
        # Exceptions connues entre noms DB et fichiers d'assets
        # Clés: slug du nom DB, Valeurs: nom de fichier (sans .png)
        mapping = {
            "archer": "archère",
            "hemomancien": "hémomencien",
            "assasin": "assassin",
            "villageois": "villagoies",
            "heros": "heros",  # si jamais utilisé
            "legende": "legende",
        }
        slug = self._slug(nom)
        if slug in mapping:
            return mapping[slug]
        # Par défaut: utiliser le nom tel quel (respect accents si présents dans fichiers)
        return nom.strip()

    def _load_icon(self, nom: str):
        key = self._nom_to_asset_key(nom)
        if key in self._icon_cache:
            return self._icon_cache[key]
        # Essayer différents chemins/noms
        candidates = [
            os.path.join("assets", "heros_icone", f"{key}.png"),
            os.path.join("assets", "heros_icone", f"{self._slug(key)}.png"),
        ]
        surf = None
        for p in candidates:
            if os.path.exists(p):
                try:
                    img = pygame.image.load(p).convert_alpha()
                    surf = pygame.transform.smoothscale(img, (self.icon_size, self.icon_size))
                    break
                except Exception:
                    pass
        self._icon_cache[key] = surf
        return surf

    def _load_splash(self, nom: str, max_h: int = 220):
        key = self._nom_to_asset_key(nom)
        if key in self._splash_cache:
            return self._splash_cache[key]
        candidates = [
            os.path.join("assets", "heros_splash", f"{key}.png"),
            os.path.join("assets", "heros_splash", f"{self._slug(key)}.png"),
        ]
        surf = None
        for p in candidates:
            if os.path.exists(p):
                try:
                    img = pygame.image.load(p).convert_alpha()
                    # Redimensionner en conservant le ratio selon la hauteur max
                    w, h = img.get_size()
                    if h > max_h:
                        scale = max_h / h
                        img = pygame.transform.smoothscale(img, (int(w * scale), int(h * scale)))
                    surf = img
                    break
                except Exception:
                    pass
        self._splash_cache[key] = surf
        return surf

    def creer_boutons_personnages(self):
        """Crée les boutons pour chaque personnage disponible (grille d'icônes horizontale)"""
        self.boutons_persos = []

        # Zone disponible: de 45 px de marge à gauche jusqu'au panneau d'équipe à droite
        left_margin = self.grid_left
        right_panel_margin = 380  # ~ largeur panneau équipe + marge
        available_w = max(300, self.game.WIDTH - (left_margin + right_panel_margin))
        start_x = left_margin + 30  # Décalage supplémentaire pour les icônes
        start_y = 200

        # Colonnes calculées selon la largeur disponible
        per_col = max(4, available_w // (self.icon_size + self.icon_padding))

        for idx, perso in enumerate(self.game.personnages_dispo):
            row = idx // per_col
            col = idx % per_col
            x = start_x + col * (self.icon_size + self.icon_padding)
            y = start_y + row * (self.icon_size + self.icon_padding)

            # Précharger l'icône pour fluidité
            _ = self._load_icon(perso.get("nom", ""))

            btn = {
                "rect": pygame.Rect(x, y, self.icon_size, self.icon_size),
                "perso": perso,
                "index": idx,
                "row": row,
                "col": col,
            }
            self.boutons_persos.append(btn)
    
    def update(self):
        pass

    def _visible_rows(self):
        """Calcule le nombre de rangées visibles selon la hauteur disponible (grille icônes)."""
        clip_height = self.game.HEIGHT - 235
        return max(1, clip_height // self.row_height)

    def _scroll_persos(self, delta: int):
        """Scroll vertical par rangées (grille icônes)."""
        # Recalculer nb colonnes actuel
        left_margin = 45
        right_panel_margin = 380
        available_w = max(300, self.game.WIDTH - (left_margin + right_panel_margin))
        per_col = max(4, available_w // (self.icon_size + self.icon_padding))
        max_rows = (len(self.game.personnages_dispo) + per_col - 1) // per_col
        visible_rows = self._visible_rows()
        max_scroll = max(0, max_rows - visible_rows)
        self.scroll_offset = max(0, min(self.scroll_offset + delta, max_scroll))
    
    def handle_events(self, event_list):
        for event in event_list:
            # Gestion de la molette pour le scroll
            if event.type == pygame.MOUSEWHEEL:
                # Scroll global : dès qu'on molette, on défile la liste
                self._scroll_persos(-event.y)
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Zone de clipping pour détecter les clics uniquement dans la zone visible
                left_margin = 45
                right_panel_margin = 380
                available_w = max(300, self.game.WIDTH - (left_margin + right_panel_margin))
                clip_rect = pygame.Rect(left_margin, 160, available_w, self.game.HEIGHT - 235)

                # Si la molette (boutons 4/5) est utilisée, gérer le scroll et ignorer la sélection
                if event.button in (4, 5):
                    delta = -1 if event.button == 4 else 1
                    self._scroll_persos(delta)
                    continue
                
                # Vérifier les clics sur les personnages (uniquement ceux visibles)
                if clip_rect.collidepoint(event.pos):
                    for btn in self.boutons_persos:
                        # Calculer la position ajustée avec le scroll
                        adjusted_y = btn["rect"].y - (self.scroll_offset * self.row_height)
                        adjusted_rect = pygame.Rect(btn["rect"].x, adjusted_y, btn["rect"].width, btn["rect"].height)

                        # Vérifier si le rectangle ajusté est visible dans la zone de clip
                        if not clip_rect.colliderect(adjusted_rect):
                            continue
                        
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
        titre_text = "HÉROS DISPONIBLES"
        titre = self.font_text.render(titre_text, True, self.style.color_primary)
        titre_shadow = self.font_text.render(titre_text, True, (30, 30, 30))
        screen.blit(titre_shadow, (self.grid_left + 2, 132))
        screen.blit(titre, (self.grid_left, 130))
        
        # Indicateur de scroll (molette)
        # Recalcule dynamique des colonnes
        left_margin = self.grid_left
        right_panel_margin = 380
        available_w = max(300, self.game.WIDTH - (left_margin + right_panel_margin))
        per_col = max(4, available_w // (self.icon_size + self.icon_padding))
        max_rows = (len(self.game.personnages_dispo) + per_col - 1) // per_col
        max_scroll = max(0, max_rows - self._visible_rows())

        
        self.popup_perso = None

        # Couleurs de bordure par rôle
        role_border_colors = {
            "attaquant": (255, 80, 80),
            "tank": (80, 150, 255),
            "support": (100, 255, 150),
            "polyvalent": (200, 120, 255),
        }

        # Zone de clipping pour le scroll (toute la hauteur disponible)
        clip_height = self.game.HEIGHT - 235
        clip_rect = pygame.Rect(left_margin, 160, available_w, clip_height)
        screen.set_clip(clip_rect)

        for btn in self.boutons_persos:
            # Calculer position avec scroll (row_height = icon + padding)
            adjusted_y = btn["rect"].y - (self.scroll_offset * self.row_height)
            rect = pygame.Rect(btn["rect"].x, adjusted_y, btn["rect"].width, btn["rect"].height)
            
            # Vérifier si le bouton est visible dans la zone de clip
            if not clip_rect.colliderect(rect):
                continue
            is_hovered = rect.collidepoint(mouse_pos) and clip_rect.collidepoint(mouse_pos)

            classe = btn['perso'].get('type_perso', btn['perso'].get('classe', 'N/A'))
            classe_key = str(classe).lower()
            border_color = role_border_colors.get(classe_key, (120, 120, 180))
            
            # Cadre d'icône façon Smash (tuile carrée + bordure)
            tile_rect = rect.inflate(14, 14)
            pygame.draw.rect(screen, (35, 40, 55), tile_rect, border_radius=10)
            border_width = 5 if is_hovered else 3
            pygame.draw.rect(screen, border_color, tile_rect, border_width, border_radius=10)

            # Icône centrée
            icon = self._load_icon(btn["perso"].get("nom", ""))
            if icon:
                icon_rect = icon.get_rect(center=rect.center)
                screen.blit(icon, icon_rect)
            else:
                # Fallback: initiale
                nom_court = btn["perso"].get("nom", "?")[:1]
                lettre = self.font_text.render(nom_court, True, (230, 230, 230))
                lettre_rect = lettre.get_rect(center=rect.center)
                screen.blit(lettre, lettre_rect)

            # Aucun label sous l'icône (désactivé)
            
            if is_hovered:
                self.popup_perso = btn["perso"]
        
        screen.set_clip(None)
    def afficher_popup_details(self, screen, perso):
        """Affiche un panneau de détails en bas de l'écran avec description et splash"""
        # Panneau en bas à gauche (réduit pour pas d'espace vide)
        margin = 40
        popup_h = 240
        popup_x = margin
        popup_w = max(420, int(self.game.WIDTH * 0.40) - margin * 2)
        popup_y = self.game.HEIGHT - popup_h - margin
        
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
        
        y_offset = popup_y + 12
        x_offset = popup_x + 14
        
        # Nom avec effet
        nom_text = self.font_text.render(perso.get("nom", "?"), True, self.style.color_primary)
        nom_shadow = self.font_text.render(perso.get("nom", "?"), True, (0, 0, 0))
        screen.blit(nom_shadow, (x_offset + 2, y_offset + 2))
        screen.blit(nom_text, (x_offset, y_offset))
        y_offset += 36
        
        # Classe sans icône
        classe = perso.get('type_perso', perso.get('classe', 'N/A'))
        classe_text = self.font_small.render(f"Classe: {classe}", True, (180, 220, 180))
        screen.blit(classe_text, (x_offset, y_offset))
        y_offset += 24
        
        # Stats avec texte simple et couleurs
        hp = perso.get('hp') or perso.get('pv') or perso.get('pv_max', 0)
        atk = perso.get('atk') or perso.get('attaque', 0)
        defense = perso.get('def') or perso.get('defense', 0)

        stats_hp = self.font_small.render(f"Vie: {hp}", True, (255, 100, 100))
        stats_atk = self.font_small.render(f"Attaque: {atk}", True, (255, 200, 100))
        stats_def = self.font_small.render(f"Defense: {defense}", True, (100, 200, 255))

        screen.blit(stats_hp, (x_offset, y_offset))
        y_offset += 22
        screen.blit(stats_atk, (x_offset, y_offset))
        y_offset += 22
        screen.blit(stats_def, (x_offset, y_offset))
        y_offset += 18

        # Préparer le splash du héros (dessiné après le texte)
        splash = self._load_splash(perso.get("nom", ""), max_h=popup_h - 40)
        splash_w = splash.get_width() if splash else 0
        
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
        # Calculer où l'image commence réellement pour étendre la description jusqu'à ce point
        if splash:
            splash_start_x = popup_x + popup_w - splash.get_width() - 20
            # La description peut s'étendre jusqu'à juste avant l'image avec un petit gap
            text_w = max(180, splash_start_x - x_offset - 12)
        else:
            text_w = popup_w - (x_offset - popup_x) - 24

        # Calcule le nombre de lignes possible selon la hauteur restante
        bottom_padding = 12
        available_h = (popup_y + popup_h - bottom_padding) - y_offset
        line_h = max(14, self.font_tiny.get_height())

        def wrap_text_height(text, font, max_width, max_height, line_height):
            # Renvoie des lignes qui tiennent dans la hauteur disponible
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
            # Tronquer selon la hauteur
            # Limiter le nombre de lignes pour garder un bloc compact
            max_lines_height = max(1, available_h // line_height)
            max_lines = min(4, max_lines_height)
            if len(lines) > max_lines:
                truncated = lines[:max_lines]
                # Ajouter ellipse sur la dernière ligne si du contenu a été coupé
                last = truncated[-1]
                ellipsis = "…"
                while font.size(last + ellipsis)[0] > max_width and len(last) > 0:
                    last = last[:-1]
                truncated[-1] = last + ellipsis
                return truncated
            return lines

        desc_lines = wrap_text_height(desc, self.font_tiny, text_w, available_h, line_h)

        desc_label = self.font_tiny.render("Description :", True, (200, 200, 100))
        screen.blit(desc_label, (x_offset, y_offset))
        y_offset += 16

        # Dessiner les lignes de description dans la colonne gauche
        for line in desc_lines:
            text_surface = self.font_tiny.render(line, True, (200, 200, 200))
            screen.blit(text_surface, (x_offset, y_offset))
            y_offset += line_h
        
        y_offset += 5

        # Dessiner le splash vers la droite du panneau
        if splash:
            splash_start_x = popup_x + popup_w - splash.get_width() - 20
            max_splash_w = splash.get_width()
            # Respecter aussi la hauteur
            w, h = splash.get_size()
            max_splash_h = popup_h - 40
            scale = min(1.0, max_splash_w / max(1, w), max_splash_h / max(1, h))
            splash_to_draw = splash
            if scale < 1.0:
                splash_to_draw = pygame.transform.smoothscale(splash, (max(1, int(w * scale)), max(1, int(h * scale))))
            sp_rect = splash_to_draw.get_rect()
            sp_rect.bottom = popup_y + popup_h - 12
            sp_rect.left = splash_start_x
            screen.blit(splash_to_draw, sp_rect)

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