# screens/__init__.py
# Permet d'importer facilement tous les écrans

from .menu import Menu
from .selection_equipe import SelectionEquipe
from .combat import Combat
from .selection_item import SelectionItem
from .selection_forme import SelectionForme
from .victoire import Victoire
from .defaite import Defaite
from .scores import Scores

__all__ = [
    'Menu',
    'SelectionEquipe',
    'Combat',
    'SelectionItem',
    'SelectionForme',
    'Victoire',
    'Defaite',
    'Scores'
]