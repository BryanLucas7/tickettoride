"""
Validators para o domínio do jogo.

Padrão GRASP: Pure Fabrication
- Separa responsabilidade de validação das entidades

Validators disponíveis:
- CompraValidator: Validação de compras de cartas (Composite)
- RouteCardValidator: Validação de cartas para conquista de rotas

Validators específicos de compra (Parte 3 - Refatoração SRP):
- JogadorValidator: Validação de existência de jogador
- CartaFechadaValidator: Validação de compra do baralho
- CartaAbertaValidator: Validação de compra das cartas abertas
"""

# Validators de compra refatorados (Parte 3)
from .compra import (
    CompraValidator, 
    CompraValidationResult,
    JogadorValidator,
    JogadorValidationResult,
    CartaFechadaValidator,
    CompraFechadaValidationResult,
    CartaAbertaValidator,
    CompraAbertaValidationResult
)

# Validator de rota (Parte 1)
from .route_card_validator import RouteCardValidator, CardValidationResult

__all__ = [
    # Composite (mantém compatibilidade)
    'CompraValidator', 
    'CompraValidationResult',
    # Validators específicos
    'JogadorValidator',
    'JogadorValidationResult',
    'CartaFechadaValidator',
    'CompraFechadaValidationResult', 
    'CartaAbertaValidator',
    'CompraAbertaValidationResult',
    # Validator de rota
    'RouteCardValidator',
    'CardValidationResult'
]
