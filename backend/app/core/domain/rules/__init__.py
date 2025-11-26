"""
Regras de negócio para cartas abertas.

GoF Pattern: Strategy
GRASP: Pure Fabrication

Este módulo contém regras que podem ser aplicadas às cartas abertas,
extraídas dos gerenciadores para melhor separação de responsabilidades.
"""

from .locomotiva_reset_rule import (
    LocomotivaResetRule, 
    CartasAbertasRule,
    NullResetRule
)

__all__ = [
    'LocomotivaResetRule',
    'CartasAbertasRule', 
    'NullResetRule'
]
