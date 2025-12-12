# Style Pixel Art - Quest Heroes

## Polices Pixel Art Recommandées

Le jeu utilise actuellement des polices système pour un effet pixel art. Pour améliorer le rendu, vous pouvez télécharger et installer une police pixel art gratuite.

### Polices Recommandées (gratuites)

1. **Press Start 2P** (recommandé)
   - Lien : https://fonts.google.com/specimen/Press+Start+2P
   - Style : 8-bit classique
   - Installation : Télécharger le fichier .ttf

2. **VT323**
   - Lien : https://fonts.google.com/specimen/VT323
   - Style : Terminal rétro
   - Installation : Télécharger le fichier .ttf

3. **Silkscreen**
   - Lien : https://fonts.google.com/specimen/Silkscreen
   - Style : Pixel art moderne
   - Installation : Télécharger le fichier .ttf

### Installation

1. Créez un dossier `assets/fonts/` dans le répertoire du jeu
2. Téléchargez la police de votre choix (fichier .ttf)
3. Renommez le fichier en `pixel.ttf`
4. Placez-le dans `assets/fonts/pixel.ttf`
5. Relancez le jeu

Le jeu chargera automatiquement la police personnalisée !

## Palette de Couleurs Utilisée

- **Or** (255, 215, 0) - Couleur primaire pour les titres
- **Violet** (200, 100, 255) - Couleur secondaire
- **Vert** (100, 255, 100) - Succès
- **Rouge** (255, 100, 100) - Danger
- **Fond sombre** (20, 20, 40) - Arrière-plan
- **Boutons normaux** (60, 60, 100)
- **Boutons survolés** (80, 80, 150)

## Éléments Stylisés

- ✅ Boutons avec bordures pixel art doubles
- ✅ Panneaux avec coins décoratifs
- ✅ Champs de saisie avec effet de luminescence
- ✅ Barres de vie avec dégradés pixelisés
- ✅ Ombres portées sur les titres
- ✅ Effets de survol cohérents

## Notes Techniques

Le fichier `pixel_style.py` contient toutes les fonctions de rendu stylisées :
- `draw_button()` - Boutons avec bordures doubles
- `draw_panel()` - Panneaux décoratifs
- `draw_text_input()` - Champs de saisie animés
- `draw_health_bar()` - Barres de vie pixelisées

Tous les écrans du jeu utilisent désormais ces fonctions pour un rendu cohérent.
