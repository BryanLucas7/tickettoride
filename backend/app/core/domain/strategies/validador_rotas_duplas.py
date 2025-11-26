"""
Validador de Rotas Duplas - Module

Implementa validação de rotas duplas para jogos com 2-3 jogadores.

Regra: Em jogos de 2-3 jogadores, apenas UMA das rotas duplas pode ser 
conquistada. Quando primeira rota dupla for conquistada, a segunda fica bloqueada.

Classes especializadas (SRP):
- RotaDupla: Entidade que representa um par de rotas (em entities/)
- RotaDuplaValidator: Responsável apenas por validação (não modifica estado)
- RotaDuplaProcessor: Responsável por processamento e bloqueio (modifica estado)
"""

# Re-exportar entidade RotaDupla do módulo de entidades
from ..entities.rota_dupla import RotaDupla

# Re-exportar classes especializadas
from .rota_dupla_validator import RotaDuplaValidator
from .rota_dupla_processor import RotaDuplaProcessor


__all__ = [
    'RotaDupla',
    'RotaDuplaValidator', 
    'RotaDuplaProcessor',
]
