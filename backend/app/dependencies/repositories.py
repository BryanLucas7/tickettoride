"""
Factories para Repository Adapters (Outbound Persistence).

Padrão GRASP: Pure Fabrication
Padrão GoF: Factory Method
Arquitetura: Hexagonal (Secondary Adapters)

Este módulo fornece factories para criar instâncias de repositories.
Pode ser facilmente trocado para usar diferentes implementações
(InMemory, Pickle, PostgreSQL, Redis, etc.)
"""

from ..core.ports.repositories.jogo_repository_port import JogoRepositoryPort
from ..adapters.outbound.persistence.pickle_jogo_repository import PickleJogoRepository

# Instância única para evitar recarregar o cache a cada requisição
_JOGO_REPOSITORY_SINGLETON: JogoRepositoryPort = PickleJogoRepository()


def get_jogo_repository() -> JogoRepositoryPort:
    """
    Factory para JogoRepository.
    
    Retorna implementação com Pickle (pode ser trocada por DB posteriormente).
    Para trocar a implementação:
    - Crie nova classe implementando JogoRepositoryPort
    - Altere apenas esta função
    
    Returns:
        Implementação de JogoRepositoryPort
    """
    return _JOGO_REPOSITORY_SINGLETON
