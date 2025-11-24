"""
GameService - Encapsula gerenciamento de jogos ativos e persistência.

Arquitetura Hexagonal:
- Usa JogoRepositoryPort (interface) para persistência
- Não depende de implementação específica (pickle, SQL, etc.)
"""
import logging
from typing import Dict, Optional

from ...core.domain.entities import Jogo
from ...core.ports.repositories.jogo_repository_port import JogoRepositoryPort


logger = logging.getLogger(__name__)


class GameService:
    """
    Service para gerenciamento de jogos.
    
    Responsabilidades:
    - Cache em memória para performance
    - Delegação para repository para persistência
    - Lógica de negócio relacionada a jogos
    
    Args:
        repository: Implementação de JogoRepositoryPort
    """
    
    def __init__(self, repository: JogoRepositoryPort):
        """
        Inicializa service com repository injetado.
        
        Args:
            repository: Implementação de JogoRepositoryPort (PickleJogoRepository, SQLJogoRepository, etc.)
        """
        self.repository = repository
        self.active_games: Dict[str, Jogo] = {}
        self._sync_from_repository()
    
    def _sync_from_repository(self) -> None:
        """Sincroniza cache com repository."""
        self.active_games.clear()
        for jogo in self.repository.listar():
            game_id = f"game-{jogo.id}" if not str(jogo.id).startswith("game-") else str(jogo.id)
            self.active_games[game_id] = jogo
        logger.info(f"Sincronizados {len(self.active_games)} jogo(s) do repository")

    def get_game(self, game_id: str) -> Optional[Jogo]:
        """
        Obtém jogo da memória ou repository.
        
        Args:
            game_id: ID do jogo
            
        Returns:
            Jogo ou None se não encontrado
        """
        # Debug temporário
        logger.info(f"🔍 DEBUG get_game - Buscando: {game_id}")
        logger.info(f"🔍 DEBUG get_game - Cache tem: {list(self.active_games.keys())}")
        
        # Tenta cache primeiro
        if game_id in self.active_games:
            logger.info(f"✅ Jogo {game_id} encontrado no cache")
            return self.active_games[game_id]
        
        # Busca no repository
        logger.info(f"🔄 Buscando {game_id} no repository...")
        jogo = self.repository.buscar(game_id)
        if jogo:
            logger.info(f"✅ Jogo {game_id} encontrado no repository, adicionando ao cache")
            self.active_games[game_id] = jogo
        else:
            logger.warning(f"❌ Jogo {game_id} NÃO encontrado nem no cache nem no repository!")
        return jogo

    def save_game(self, game_id: str, jogo: Jogo) -> None:
        """
        Salva jogo na memória e repository.
        
        Args:
            game_id: ID do jogo
            jogo: Instância do jogo
        """
        self.active_games[game_id] = jogo
        self.repository.salvar(jogo)
        logger.debug(f"Jogo {game_id} salvo")
