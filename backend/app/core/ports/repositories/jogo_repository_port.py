"""
JogoRepository Port - Interface para persistência de jogos

Define o contrato que implementações de persistência devem seguir.
"""

from abc import ABC, abstractmethod
from typing import Optional, List

from app.core.domain.entities.jogo import Jogo


class JogoRepositoryPort(ABC):
    """
    Port (Interface) para repositório de jogos.
    
    Implementações podem usar:
    - Pickle (PickleJogoRepository)
    - SQL (SQLJogoRepository)
    - NoSQL (MongoJogoRepository)
    - In-memory (InMemoryJogoRepository - para testes)
    """

    @abstractmethod
    def salvar(self, jogo: Jogo) -> None:
        """
        Persiste um jogo.
        
        Args:
            jogo: Instância do jogo a ser salva
            
        Raises:
            PersistenceError: Se houver erro ao salvar
        """
        pass

    @abstractmethod
    def buscar(self, game_id: str) -> Optional[Jogo]:
        """
        Busca um jogo pelo ID.
        
        Args:
            game_id: ID único do jogo
            
        Returns:
            Instância do jogo ou None se não encontrado
            
        Raises:
            PersistenceError: Se houver erro ao buscar
        """
        pass

    @abstractmethod
    def listar(self) -> List[Jogo]:
        """
        Lista todos os jogos salvos.
        
        Returns:
            Lista de jogos (pode ser vazia)
            
        Raises:
            PersistenceError: Se houver erro ao listar
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def existe(self, game_id: str) -> bool:
        """
        Verifica se um jogo existe.
        
        Args:
            game_id: ID único do jogo
            
        Returns:
            True se existe, False caso contrário
        """
        pass
