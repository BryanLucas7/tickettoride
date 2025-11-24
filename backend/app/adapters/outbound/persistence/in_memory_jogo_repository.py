"""
InMemoryJogoRepository - Implementação em memória para testes

Repository fake que não persiste nada, ideal para testes unitários.
"""

import logging
from typing import Optional, List, Dict
from ....core.ports.repositories.jogo_repository_port import JogoRepositoryPort

# Import condicional
try:
    from ....models.entities.jogo import Jogo
except ImportError:
    from app.core.domain.entities.jogo import Jogo


logger = logging.getLogger(__name__)


class InMemoryJogoRepository(JogoRepositoryPort):
    """
    Implementação in-memory de JogoRepositoryPort para testes.
    
    Não persiste em disco, apenas mantém jogos em memória.
    Perfeito para:
    - Testes unitários rápidos
    - Testes de integração sem dependência de I/O
    - Desenvolvimento local sem poluir disco
    """
    
    def __init__(self):
        """Inicializa repository vazio."""
        self._games: Dict[str, Jogo] = {}
        logger.debug("InMemoryJogoRepository inicializado")
    
    def salvar(self, jogo: Jogo) -> None:
        """Salva jogo em memória."""
        game_id = f"game-{jogo.id}" if not str(jogo.id).startswith("game-") else str(jogo.id)
        self._games[game_id] = jogo
        logger.debug("Jogo salvo em memória: %s", game_id)
    
    def buscar(self, game_id: str) -> Optional[Jogo]:
        """Busca jogo na memória."""
        jogo = self._games.get(game_id)
        logger.debug("Buscar jogo %s: %s", game_id, "encontrado" if jogo else "não encontrado")
        return jogo
    
    def listar(self) -> List[Jogo]:
        """Lista todos os jogos em memória."""
        jogos = list(self._games.values())
        logger.debug("Listando %d jogo(s) da memória", len(jogos))
        return jogos
    
    def deletar(self, game_id: str) -> bool:
        """Remove jogo da memória."""
        if game_id in self._games:
            del self._games[game_id]
            logger.debug("Jogo deletado da memória: %s", game_id)
            return True
        logger.debug("Jogo não encontrado para deletar: %s", game_id)
        return False
    
    def existe(self, game_id: str) -> bool:
        """Verifica se jogo existe na memória."""
        exists = game_id in self._games
        logger.debug("Jogo %s existe: %s", game_id, exists)
        return exists
    
    def limpar_todos(self) -> None:
        """Limpa todos os jogos da memória."""
        count = len(self._games)
        self._games.clear()
        logger.debug("Limpos %d jogo(s) da memória", count)
    
    def contar(self) -> int:
        """Retorna quantidade de jogos em memória (útil para testes)."""
        return len(self._games)
