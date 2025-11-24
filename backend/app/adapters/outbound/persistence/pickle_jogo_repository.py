"""
PickleJogoRepository - Implementação de persistência usando Pickle

Adapter que implementa JogoRepositoryPort usando serialização pickle.
"""

import pickle
import logging
from pathlib import Path
from typing import Optional, List, Dict
from ....core.ports.repositories.jogo_repository_port import JogoRepositoryPort

# Import condicional para evitar erro circular
try:
    from ....models.entities.jogo import Jogo
except ImportError:
    from app.core.domain.entities.jogo import Jogo


logger = logging.getLogger(__name__)


class PickleJogoRepository(JogoRepositoryPort):
    """
    Implementação de JogoRepositoryPort usando pickle para persistência.
    
    Características:
    - Armazena jogos em arquivo .pkl único
    - Cache em memória para performance
    - Thread-safe (depende do uso)
    
    Args:
        cache_file: Caminho do arquivo pickle (default: .games_cache.pkl)
    """
    
    def __init__(self, cache_file: Optional[Path] = None):
        """
        Inicializa o repository com arquivo de cache.
        
        Args:
            cache_file: Caminho do arquivo pickle. Se None, usa padrão.
        """
        if cache_file is None:
            # Usa o mesmo caminho do código atual
            cache_file = Path(__file__).resolve().parents[3] / ".games_cache.pkl"
        
        self.cache_file = cache_file
        self._games_cache: Dict[str, Jogo] = {}
        self._load_from_disk()
    
    def _load_from_disk(self) -> None:
        """Carrega jogos do arquivo pickle para o cache em memória."""
        if not self.cache_file.exists():
            logger.info("Cache file não existe ainda: %s", self.cache_file)
            return
        
        try:
            with self.cache_file.open("rb") as f:
                cached_games = pickle.load(f)
            
            if isinstance(cached_games, dict):
                self._games_cache.clear()
                self._games_cache.update(cached_games)
                logger.info("Carregados %d jogo(s) do cache", len(self._games_cache))
        except Exception as exc:
            logger.warning("Falha ao carregar cache: %s", exc)
            self._games_cache = {}
    
    def _persist_to_disk(self) -> None:
        """Persiste o cache em memória para o arquivo pickle."""
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            with self.cache_file.open("wb") as f:
                pickle.dump(self._games_cache, f)
            logger.debug("Cache persistido: %d jogo(s)", len(self._games_cache))
        except Exception as exc:
            logger.error("Falha ao persistir cache: %s", exc)
            raise PersistenceError(f"Erro ao salvar jogos: {exc}") from exc
    
    def salvar(self, jogo: Jogo) -> None:
        """
        Persiste um jogo.
        
        Args:
            jogo: Instância do jogo a ser salva
            
        Raises:
            PersistenceError: Se houver erro ao salvar
        """
        game_id = f"game-{jogo.id}" if not str(jogo.id).startswith("game-") else str(jogo.id)
        self._games_cache[game_id] = jogo
        self._persist_to_disk()
        logger.info("Jogo salvo: %s", game_id)
    
    def buscar(self, game_id: str) -> Optional[Jogo]:
        """
        Busca um jogo pelo ID.
        
        Args:
            game_id: ID único do jogo
            
        Returns:
            Instância do jogo ou None se não encontrado
        """
        jogo = self._games_cache.get(game_id)
        if jogo:
            logger.debug("Jogo encontrado no cache: %s", game_id)
        else:
            logger.debug("Jogo não encontrado: %s", game_id)
        return jogo
    
    def listar(self) -> List[Jogo]:
        """
        Lista todos os jogos salvos.
        
        Returns:
            Lista de jogos (pode ser vazia)
        """
        jogos = list(self._games_cache.values())
        logger.debug("Listando %d jogo(s)", len(jogos))
        return jogos
    
    def deletar(self, game_id: str) -> bool:
        """
        Remove um jogo da persistência.
        
        Args:
            game_id: ID único do jogo
            
        Returns:
            True se deletado, False se não encontrado
            
        Raises:
            PersistenceError: Se houver erro ao deletar
        """
        if game_id in self._games_cache:
            del self._games_cache[game_id]
            self._persist_to_disk()
            logger.info("Jogo deletado: %s", game_id)
            return True
        
        logger.warning("Tentativa de deletar jogo inexistente: %s", game_id)
        return False
    
    def existe(self, game_id: str) -> bool:
        """
        Verifica se um jogo existe.
        
        Args:
            game_id: ID único do jogo
            
        Returns:
            True se existe, False caso contrário
        """
        exists = game_id in self._games_cache
        logger.debug("Jogo %s existe: %s", game_id, exists)
        return exists
    
    def limpar_todos(self) -> None:
        """
        Remove todos os jogos (útil para testes).
        
        Raises:
            PersistenceError: Se houver erro ao limpar
        """
        self._games_cache.clear()
        self._persist_to_disk()
        logger.info("Todos os jogos foram removidos")


class PersistenceError(Exception):
    """Exceção levantada quando há erro de persistência."""
    pass
