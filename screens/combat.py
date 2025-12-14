import pygame
from attaques import obtenir_attaques_disponibles, gerer_cooldown_attaque
from pixel_style import pixel_style

class Combat:
    def __init__(self, game):
        self.game = game
        self.style = pixel_style
        self.font_title = self.style.font_title
        self.font_text = self.style.font_text
        self.font_small = self.style.font_small
        self.font_tiny = self.style.font_tiny
        
        # Charger l'image du lieu et le sprite du monstre
        self.background = None
        self.monstre_sprite = None
        import os
        
        monstre = game.obtenir_monstre_actuel()
        if monstre:
            # Charger l'image du lieu
            lieu = getattr(monstre, "lieu", "prairie")
            try:
                lieu_path = os.path.join("assets", "lieux", f"{lieu}.png")
                if os.path.exists(lieu_path):
                    self.background = pygame.image.load(lieu_path)
                    self.background = pygame.transform.scale(self.background, (game.WIDTH, game.HEIGHT))
            except Exception as e:
                print(f"Erreur chargement lieu {lieu}: {e}")
            
            # Charger le sprite du monstre
            monstre_nom = monstre.nom.lower()
            try:
                sprite_path = os.path.join("assets", "monstres", f"{monstre_nom}.png")
                if os.path.exists(sprite_path):
                    self.monstre_sprite = pygame.image.load(sprite_path)
                    self.monstre_sprite = pygame.transform.scale(self.monstre_sprite, (450, 450))
            except Exception as e:
                print(f"Erreur chargement sprite monstre {monstre_nom}: {e}")
        
        # État du combat
        self.hero_actuel_index = 0
        self.en_attente_action = True
        self.messages = []
        self.message_timer = 0
        
        # Boutons d'attaque
        self.boutons_attaques = []
        self.creer_boutons_attaques()

        # Mémo pour les métamorphoses
        self.pending_metamorphose = None
        
        # Bouton passer le tour (aligné avec les attaques) - hauteur réduite
        self.btn_passer = pygame.Rect(self.game.WIDTH - 240, 800, 200, 70)
        
    def creer_boutons_attaques(self):
        """Crée les boutons pour les attaques du héros actuel"""
        self.boutons_attaques = []
        
        while self.hero_actuel_index < len(self.game.equipe):
            hero = self.game.equipe[self.hero_actuel_index]
            if hero.est_vivant():
                break
            self.hero_actuel_index += 1
        
        if self.hero_actuel_index >= len(self.game.equipe):
            self.tour_monstre()
            return
        
        hero = self.game.equipe[self.hero_actuel_index]
        attaques = obtenir_attaques_disponibles(hero)
        
        y_start = 715
        espacement = 390
        for idx, (type_attaque, attaque_info) in enumerate(attaques):
            btn = {
                "rect": pygame.Rect(80 + idx * espacement, y_start, 375, 155),
                "type": type_attaque,
                "info": attaque_info,
                "cooldown": hero.cooldowns.get(type_attaque, 0)
            }
            self.boutons_attaques.append(btn)
    
    def passer_au_hero_suivant(self):
        """Passe au héros suivant qui peut agir"""
        self.hero_actuel_index += 1
        
        while self.hero_actuel_index < len(self.game.equipe):
            if self.game.equipe[self.hero_actuel_index].est_vivant():
                break
            self.hero_actuel_index += 1
        
        if self.hero_actuel_index >= len(self.game.equipe):
            self.tour_monstre()
        else:
            self.creer_boutons_attaques()
    
    def tour_monstre(self):
        """Exécute le tour du monstre"""
        monstre = self.game.obtenir_monstre_actuel()
        if not monstre:
            return
        
        resultat = self.game.tour_monstre(monstre)
        self.messages = resultat["messages"]
        self.message_timer = 180
        
        if self.game.verifier_defaite():
            from screens.defaite import Defaite
            self.game.change_screen(Defaite)
            return
        
        for hero in self.game.equipe:
            hero.reduire_cooldowns()
        
        self.game.tour += 1
        if hasattr(self.game, "tours_cumule"):
            self.game.tours_cumule += 1
        self.hero_actuel_index = 0
        self.en_attente_action = True
        self.creer_boutons_attaques()
    
    def update(self):
        pass
    
    def handle_events(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.messages:
                    message_rect = pygame.Rect(410, 260, 780, 350)
                    if message_rect.collidepoint(event.pos):
                        self.messages = []
                        return
        
        if not self.en_attente_action:
            return
        
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in self.boutons_attaques:
                    if btn["rect"].collidepoint(event.pos) and btn["cooldown"] == 0:
                        resultat = self.executer_attaque(self.hero_actuel_index, btn["type"], btn["info"])
                        
                        if resultat.get("selection_forme"):
                            self.pending_metamorphose = {"type": btn["type"], "info": btn["info"]}
                            self.ouvrir_selection_forme(resultat)
                            return
                        
                        self.traiter_resultat_attaque(resultat)
                        break
                
                if self.btn_passer.collidepoint(event.pos):
                    self.passer_au_hero_suivant()
    
    def ouvrir_selection_forme(self, resultat):
        """Ouvre l'écran de sélection de forme pour la druidesse"""
        hero = self.game.equipe[self.hero_actuel_index]
        monstre = self.game.obtenir_monstre_actuel()
        formes = resultat.get("formes_disponibles", [])
        
        self.messages = resultat.get("messages", [])
        self.message_timer = 120
        
        from screens.selection_forme import SelectionForme
        
        def callback_retour(msg_transfo):
            if self.pending_metamorphose:
                hero = self.game.equipe[self.hero_actuel_index]
                gerer_cooldown_attaque(hero, self.pending_metamorphose["type"], self.pending_metamorphose["info"])
                self.pending_metamorphose = None

            self.messages = [msg_transfo]
            self.message_timer = 120
            self.game.change_screen(Combat)
            self.passer_au_hero_suivant()
        
        selection_forme = SelectionForme(
            self.game, 
            hero, 
            monstre, 
            self.game.equipe, 
            formes, 
            callback_retour
        )
        self.game.change_screen(lambda game: selection_forme)
    
    def executer_attaque(self, hero_index, type_attaque, attaque_info):
        """Exécute l'attaque du héros spécifié par index"""
        hero = self.game.equipe[hero_index]
        monstre = self.game.obtenir_monstre_actuel()
        
        resultat = self.game.tour_hero_unique(hero, monstre, type_attaque, attaque_info)
        return resultat

    def traiter_resultat_attaque(self, resultat):
        """Traite le résultat d'une attaque normale"""
        self.messages = resultat.get("messages", [])
        self.message_timer = 120

        if resultat.get("ouvrir_selection_item") and resultat.get("item_cree"):
            from screens.selection_item import SelectionItem
            self.game.change_screen(lambda g: SelectionItem(g, item_override=resultat["item_cree"], retour_combat=True))
            return
        
        if not resultat.get("monstre_vivant", True):
            self.game.victoires += 1
            from screens.selection_item import SelectionItem
            self.game.change_screen(SelectionItem)
            return
        
        self.passer_au_hero_suivant()
    
    def draw_pixel_box(self, screen, rect, bg_color, border_color, thickness=3):
        """Dessine une boîte style pixel art"""
        # Fond
        pygame.draw.rect(screen, bg_color, rect)
        # Bordure externe
        pygame.draw.rect(screen, border_color, rect, thickness)
        # Bordure interne pour effet de profondeur
        inner = pygame.Rect(rect.x + thickness, rect.y + thickness, 
                           rect.width - thickness*2, rect.height - thickness*2)
        highlight = tuple(min(c + 20, 255) for c in border_color)
        pygame.draw.rect(screen, highlight, inner, 1)
    
    def draw_hp_bar(self, screen, x, y, width, height, current, maximum, bar_color):
        """Dessine une barre de vie RPG"""
        percent = current / maximum if maximum > 0 else 0
        
        # Fond noir
        pygame.draw.rect(screen, (20, 20, 20), (x, y, width, height))
        
        # Barre de vie
        if percent > 0:
            bar_width = int(width * percent)
            pygame.draw.rect(screen, bar_color, (x, y, bar_width, height))
            
            # Brillance sur la moitié supérieure
            shine_color = tuple(min(c + 40, 255) for c in bar_color)
            pygame.draw.rect(screen, shine_color, (x, y, bar_width, height // 2))
        
        # Bordure
        pygame.draw.rect(screen, (180, 180, 180), (x, y, width, height), 2)
    
    def draw_stat_box(self, screen, x, y, label, value, color):
        """Dessine une boîte de statistique"""
        width, height = 90, 28
        
        # Fond avec dégradé subtil
        bg_color = (25, 25, 35)
        pygame.draw.rect(screen, bg_color, (x, y, width, height), border_radius=4)
        
        # Bordure douce
        border_color = tuple(min(c + 20, 255) for c in color)
        pygame.draw.rect(screen, border_color, (x, y, width, height), 1, border_radius=4)
        
        # Label
        label_surf = self.font_tiny.render(label, True, (160, 160, 170))
        screen.blit(label_surf, (x + 6, y + 6))
        
        # Valeur
        value_surf = self.font_small.render(str(value), True, color)
        screen.blit(value_surf, (x + width - value_surf.get_width() - 8, y + 4))
    
    def draw(self, screen):
        # Fond du lieu
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((30, 30, 60))
        
        # Overlay pour lisibilité
        overlay = pygame.Surface((self.game.WIDTH, self.game.HEIGHT))
        overlay.set_alpha(160)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Sprite du monstre avec effet de dommages
        if self.monstre_sprite:
            sprite_x = self.game.WIDTH - 470
            sprite_y = 140
            monstre = self.game.obtenir_monstre_actuel()
            if monstre and monstre.pv < monstre.pv_max:
                ratio = 1.0 - (monstre.pv / monstre.pv_max)
                sprite = self.monstre_sprite.copy()
                try:
                    import numpy as np
                    arr = pygame.surfarray.pixels_alpha(sprite)
                    mask = arr > 0
                    red_overlay = pygame.surfarray.pixels3d(sprite)
                    red_intensity = int(40 + 140 * ratio)
                    red_overlay[...,0][mask] = np.minimum(255, red_overlay[...,0][mask] + red_intensity)
                    del arr
                    del red_overlay
                except Exception:
                    pass
                screen.blit(sprite, (sprite_x, sprite_y))
            else:
                screen.blit(self.monstre_sprite, (sprite_x, sprite_y))
        
        # Bandeau de titre
        title_rect = pygame.Rect(0, 0, self.game.WIDTH, 45)
        self.draw_pixel_box(screen, title_rect, (25, 20, 40), (200, 180, 100), 4)
        
        title = self.font_text.render(f"COMBAT - Tour {self.game.tour}", True, (255, 220, 100))
        title_x = self.game.WIDTH // 2 - title.get_width() // 2
        # Ombre
        shadow = self.font_text.render(f"COMBAT - Tour {self.game.tour}", True, (60, 40, 0))
        screen.blit(shadow, (title_x + 2, 9))
        screen.blit(title, (title_x, 7))
        
        # Afficher l'équipe
        self.afficher_equipe(screen)
        
        # Afficher le monstre
        self.afficher_monstre(screen)
        
        # Bannière du héros actuel - élégante
        if self.hero_actuel_index < len(self.game.equipe):
            hero = self.game.equipe[self.hero_actuel_index]
            if hero.est_vivant():
                # Bannière moderne
                banner_rect = pygame.Rect(410, 625, 780, 40)
                pygame.draw.rect(screen, (38, 33, 48), banner_rect, border_radius=6)
                pygame.draw.rect(screen, (210, 190, 90), banner_rect, 2, border_radius=6)
                
                # Flèche et nom stylisés
                hero_text = self.font_text.render(f"▶ Tour de {hero.nom.upper()}", True, (255, 255, 150))
                screen.blit(hero_text, (420, 630))
                
                # Stacks badge
                if hasattr(hero, 'stack') and hero.stack > 0:
                    stack_bg = pygame.Rect(banner_rect.x + banner_rect.width - 150, banner_rect.y + 4, 140, 32)
                    pygame.draw.rect(screen, (50, 40, 25), stack_bg, border_radius=4)
                    pygame.draw.rect(screen, (200, 160, 80), stack_bg, 2, border_radius=4)
                    stack_text = self.font_small.render(f"Stacks: {hero.stack}", True, (255, 200, 100))
                    stack_x = stack_bg.x + (stack_bg.width - stack_text.get_width()) // 2
                    screen.blit(stack_text, (stack_x, stack_bg.y + 5))
        
        # Boutons d'attaque - repositionnés
        mouse_pos = pygame.mouse.get_pos()

        for btn in self.boutons_attaques:
            # Couleurs selon état
            if btn["cooldown"] > 0:
                bg_color = (50, 50, 60)
                border_color = (90, 90, 110)
                text_color = (140, 140, 150)
            elif btn["rect"].collidepoint(mouse_pos):
                bg_color = (80, 70, 120)
                border_color = (180, 160, 220)
                text_color = (255, 255, 255)
            else:
                bg_color = (60, 55, 90)
                border_color = (130, 120, 180)
                text_color = (230, 230, 230)
            
            # Dessiner le bouton
            self.draw_pixel_box(screen, btn["rect"], bg_color, border_color, 3)
            
            # Nom de l'attaque
            nom = self.font_text.render(btn["info"].get("nom", "Attaque"), True, text_color)
            screen.blit(nom, (btn["rect"].x + 10, btn["rect"].y + 10))
            
            # Description (wrapping) - optimisée
            desc = btn["info"].get("description", "")
            if desc:
                words = desc.split()
                lines = []
                current_line = ""
                max_width = btn["rect"].width - 20
                
                for word in words:
                    test_line = f"{current_line} {word}".strip()
                    if self.font_tiny.size(test_line)[0] <= max_width:
                        current_line = test_line
                    else:
                        if current_line:
                            lines.append(current_line)
                        current_line = word
                if current_line:
                    lines.append(current_line)
                
                y_offset = btn["rect"].y + 40
                for i, line in enumerate(lines[:3]):  # Max 3 lignes
                    if y_offset < btn["rect"].y + btn["rect"].height - 35:
                        txt = self.font_tiny.render(line, True, (200, 200, 210))
                        screen.blit(txt, (btn["rect"].x + 10, y_offset))
                        y_offset += 20
            
            # Statut (cooldown ou prêt)
            status_y = btn["rect"].y + btn["rect"].height - 28
            if btn["cooldown"] > 0:
                cd_rect = pygame.Rect(btn["rect"].x + 6, status_y, btn["rect"].width - 12, 24)
                pygame.draw.rect(screen, (70, 40, 40), cd_rect)
                pygame.draw.rect(screen, (180, 80, 80), cd_rect, 2)
                cd_text = self.font_tiny.render(f"Attente: {btn['cooldown']}", True, (255, 150, 150))
                screen.blit(cd_text, (cd_rect.x + 8, cd_rect.y + 5))
            else:
                ready_rect = pygame.Rect(btn["rect"].x + 6, status_y, btn["rect"].width - 12, 24)
                pygame.draw.rect(screen, (40, 70, 40), ready_rect)
                pygame.draw.rect(screen, (100, 200, 100), ready_rect, 2)
                ready_text = self.font_tiny.render("Pret", True, (150, 255, 150))
                screen.blit(ready_text, (ready_rect.x + 8, ready_rect.y + 5))
        
        # Bouton passer
        is_hover = self.btn_passer.collidepoint(mouse_pos)
        btn_color = (90, 60, 60) if is_hover else (70, 50, 50)
        border_color = (180, 120, 120) if is_hover else (140, 100, 100)
        
        self.draw_pixel_box(screen, self.btn_passer, btn_color, border_color, 2)
        
        pass_text = self.font_small.render("PASSER", True, (255, 200, 200))
        text_x = self.btn_passer.x + (self.btn_passer.width - pass_text.get_width()) // 2
        text_y = self.btn_passer.y + (self.btn_passer.height - pass_text.get_height()) // 2
        # Ombre
        shadow = self.font_small.render("PASSER", True, (40, 20, 20))
        screen.blit(shadow, (text_x + 1, text_y + 1))
        screen.blit(pass_text, (text_x, text_y))
        
        # Messages
        self.afficher_messages(screen)
    
    def afficher_equipe(self, screen):
        """Affiche l'équipe à gauche - version épurée sans case"""
        x = 50
        y = 70
        
        # Titre sans case
        title = self.font_text.render("VOTRE EQUIPE", True, (150, 255, 150))
        screen.blit(title, (x, y))
        y += 35
        
        for idx, hero in enumerate(self.game.equipe):
            # Héros sans case - épuré
            hero_h = 115
            hero_x = x
            hero_y = y
            
            # Couleurs selon état
            if not hero.est_vivant():
                name_color = (110, 110, 110)
            elif idx == self.hero_actuel_index:
                name_color = (255, 255, 150)
                # Indicateur subtil pour le héros actuel
                indicator = pygame.Surface((4, hero_h - 10), pygame.SRCALPHA)
                indicator.fill((220, 200, 100, 200))
                screen.blit(indicator, (hero_x - 8, hero_y + 5))
            else:
                name_color = (220, 220, 220)
            
            # Nom du héros
            nom = self.font_text.render(hero.nom, True, name_color)
            screen.blit(nom, (hero_x, hero_y))
            
            # Stacks à droite du nom
            if hasattr(hero, 'stack') and hero.stack > 0:
                stack = self.font_small.render(f"x{hero.stack}", True, (255, 200, 100))
                stack_x = hero_x + 280 - stack.get_width()
                screen.blit(stack, (stack_x, hero_y + 3))
            
            # Stats ATK et DEF - inline simples
            stats_y = hero_y + 28
            atk_text = self.font_small.render(f"ATK {hero.atk}", True, (255, 150, 150))
            screen.blit(atk_text, (hero_x, stats_y))
            
            def_text = self.font_small.render(f"DEF {hero.defense}", True, (150, 200, 255))
            screen.blit(def_text, (hero_x + 90, stats_y))
            
            # Barre de vie élégante
            hp_y = hero_y + 52
            hp_bar_width = 240
            self.draw_hp_bar(screen, hero_x, hp_y, hp_bar_width, 22, hero.pv, hero.pv_max, (90, 220, 90))
            
            # Texte HP à droite de la barre
            hp_text = self.font_small.render(f"{hero.pv}/{hero.pv_max}", True, (255, 255, 255))
            screen.blit(hp_text, (hero_x + hp_bar_width + 8, hp_y + 2))
            
            # Statuts/Buffs
            if hasattr(hero, 'status') and hero.status:
                status_y = hero_y + 82
                statuts = []
                for s in hero.status:
                    t = s.get('tours_restants', 0)
                    if t > 0:
                        statuts.append(f"{s.get('stat', '?')[:4]}({t})")
                
                if statuts:
                    status_txt = " • ".join(statuts[:3])
                    status_surf = self.font_tiny.render(status_txt, True, (255, 180, 150))
                    screen.blit(status_surf, (hero_x, status_y))
            
            # Ligne de séparation subtile entre héros
            if idx < len(self.game.equipe) - 1:
                sep_y = hero_y + hero_h
                pygame.draw.line(screen, (60, 60, 80), (hero_x, sep_y), (hero_x + 300, sep_y), 1)
            
            y += hero_h + 12
    
    def afficher_monstre(self, screen):
        """Affiche le monstre au centre-droit - version épurée"""
        monstre = self.game.obtenir_monstre_actuel()
        if not monstre:
            return
        
        # Position plus à droite
        x = 680
        y = 65

        # Nom avec effet d'ombre prononcé - taille réduite
        nom = self.font_text.render(monstre.nom.upper(), True, (255, 120, 120))
        shadow = self.font_text.render(monstre.nom.upper(), True, (40, 10, 10))
        # Double ombre pour plus de profondeur
        screen.blit(shadow, (x + 2, y + 2))
        shadow2 = self.font_text.render(monstre.nom.upper(), True, (60, 15, 15))
        screen.blit(shadow2, (x + 1, y + 1))
        screen.blit(nom, (x, y))

        # Barre de vie élégante sans case
        bar_y = y + 40
        bar_width = 420
        
        # Fond sombre derrière la barre pour contraste
        bg_bar = pygame.Surface((bar_width + 100, 50), pygame.SRCALPHA)
        bg_bar.fill((0, 0, 0, 100))
        screen.blit(bg_bar, (x - 5, bar_y - 5))
        
        # Barre de vie principale
        self.draw_hp_bar(screen, x, bar_y, bar_width, 36, monstre.pv, monstre.pv_max, (220, 60, 60))
        
        # HP texte bien visible avec ombre
        hp_text = self.font_text.render(f"{monstre.pv}/{monstre.pv_max}", True, (255, 255, 255))
        hp_shadow = self.font_text.render(f"{monstre.pv}/{monstre.pv_max}", True, (0, 0, 0))
        hp_x = x + bar_width + 15
        screen.blit(hp_shadow, (hp_x + 2, bar_y + 7))
        screen.blit(hp_text, (hp_x, bar_y + 5))

        # Stats épurées sous la barre
        stats_y = bar_y + 50
        self.draw_stat_box(screen, x, stats_y, "ATK", monstre.atk, (255, 150, 150))
        self.draw_stat_box(screen, x + 105, stats_y, "DEF", monstre.defense, (150, 200, 255))

        # Statuts avec fond semi-transparent
        if hasattr(monstre, 'status') and monstre.status:
            statuts = []
            for s in monstre.status:
                t = s.get('tours_restants', 0)
                if t > 0:
                    statuts.append(f"{s.get('stat', '?')[:4].capitalize()}({t})")
            
            if statuts:
                status_y = stats_y + 42
                status_txt = " • ".join(statuts[:3])
                status_surf = self.font_small.render(status_txt, True, (255, 170, 170))
                # Fond pour lisibilité
                status_bg = pygame.Surface((status_surf.get_width() + 16, 26), pygame.SRCALPHA)
                status_bg.fill((0, 0, 0, 120))
                screen.blit(status_bg, (x - 3, status_y - 3))
                screen.blit(status_surf, (x, status_y))
    
    def afficher_messages(self, screen):
        """Affiche les messages de combat"""
        if not self.messages:
            return
        
        # Panneau de messages - repositionné
        msg_rect = pygame.Rect(410, 260, 780, 350)
        self.draw_pixel_box(screen, msg_rect, (20, 20, 30), (150, 150, 200), 3)
        
        x = msg_rect.x + 15
        y = msg_rect.y + 12
        
        # Titre
        title = self.font_text.render("ACTIONS DE COMBAT", True, (200, 200, 255))
        screen.blit(title, (x, y))
        y += 35
        
        # Messages
        for msg in self.messages[-3:]:
            icon = ">"
            if "degats" in msg.lower() or "dommages" in msg.lower():
                icon = "-"
            elif "soigne" in msg.lower() or "recupere" in msg.lower():
                icon = "+"
            elif "rate" in msg.lower():
                icon = "x"
            elif "critique" in msg.lower():
                icon = "!"
            
            text = self.font_small.render(f"{icon} {msg}", True, (255, 255, 255))
            screen.blit(text, (x, y))
            y += 32
        
        # Hint
        hint = self.font_tiny.render("[ Cliquez pour continuer ]", True, (180, 180, 200))
        screen.blit(hint, (msg_rect.x + msg_rect.width - hint.get_width() - 15, msg_rect.y + msg_rect.height - 25))