"""
Factory para criação de estratégias de validação de rotas.

GoF Pattern: Factory Method
- Encapsula a criação de objetos Strategy
- Determina automaticamente qual estratégia usar baseado na cor da rota

Refatoração SRP: Factory extraída de rota_validation_strategy.py para
separar responsabilidade de criação da responsabilidade de validação.

Uso:
    from .rota_validation_factory import criar_estrategia_validacao
    
    estrategia = criar_estrategia_validacao(rota.cor)
    resultado = estrategia.validar(cartas_jogador, comprimento, cor_rota)
"""

from app.core.domain.entities.cor import Cor
from .rota_validation_strategy import (
    RotaValidationStrategy,
    RotaColoridaStrategy,
    RotaCinzaStrategy
)


def criar_estrategia_validacao(cor_rota: Cor) -> RotaValidationStrategy:
    """
    Factory method para criar estratégia apropriada de validação.
    
    GoF Factory Method Pattern:
    - Encapsula decisão de qual classe concreta instanciar
    - Cliente não precisa conhecer as classes concretas
    - Facilita adição de novas estratégias sem modificar clientes
    
    Args:
        cor_rota: Cor da rota a ser validada
                 - Cor.CINZA: Retorna RotaCinzaStrategy (qualquer cor)
                 - Outras cores: Retorna RotaColoridaStrategy (cor específica)
        
    Returns:
        Estratégia apropriada para validar a rota
        
    Examples:
        >>> estrategia = criar_estrategia_validacao(Cor.VERMELHO)
        >>> isinstance(estrategia, RotaColoridaStrategy)
        True
        
        >>> estrategia = criar_estrategia_validacao(Cor.CINZA)
        >>> isinstance(estrategia, RotaCinzaStrategy)
        True
    """
    if cor_rota == Cor.CINZA:
        return RotaCinzaStrategy()
    else:
        return RotaColoridaStrategy()


# Aliases para conveniência
def criar_estrategia_rota_colorida() -> RotaColoridaStrategy:
    """
    Cria estratégia para rotas coloridas.
    
    Útil quando já se sabe que a rota tem cor específica.
    """
    return RotaColoridaStrategy()


def criar_estrategia_rota_cinza() -> RotaCinzaStrategy:
    """
    Cria estratégia para rotas cinzas.
    
    Útil quando já se sabe que a rota é cinza.
    """
    return RotaCinzaStrategy()
