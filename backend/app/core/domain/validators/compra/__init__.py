"""
Validators de compra de cartas - Composite Pattern.

Refatoração SRP: CompraValidator dividido em validators específicos:
- JogadorValidator: valida existência de jogador
- CartaFechadaValidator: valida regras de compra do baralho
- CartaAbertaValidator: valida regras de compra das cartas visíveis
- CompraValidator: Composite que coordena os validators

Padrões aplicados:
- GoF Composite: CompraValidator agrupa validators específicos
- GRASP Pure Fabrication: Validators são classes artificiais para validação
"""

from .jogador_validator import JogadorValidator, JogadorValidationResult
from .carta_fechada_validator import CartaFechadaValidator, CompraFechadaValidationResult
from .carta_aberta_validator import CartaAbertaValidator, CompraAbertaValidationResult
from .compra_validator_composite import CompraValidator, CompraValidationResult

__all__ = [
    'JogadorValidator',
    'JogadorValidationResult',
    'CartaFechadaValidator', 
    'CompraFechadaValidationResult',
    'CartaAbertaValidator',
    'CompraAbertaValidationResult',
    'CompraValidator',
    'CompraValidationResult'
]
