"""
Persistence Adapters - Adaptadores de persistência

Implementam os repository ports usando tecnologias específicas.

Implementações:
- PickleJogoRepository: Usa pickle para serializar jogos em arquivos
- InMemoryJogoRepository: Armazena em memória (para testes)
"""

from .pickle_jogo_repository import PickleJogoRepository, PersistenceError
from .in_memory_jogo_repository import InMemoryJogoRepository

__all__ = [
    "PickleJogoRepository",
    "InMemoryJogoRepository",
    "PersistenceError",
]
