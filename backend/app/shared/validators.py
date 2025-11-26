"""
GameValidators - Validadores centralizados para entidades do jogo.

Implementa Pure Fabrication (GRASP) para eliminar duplicação de código
de validação em todo o sistema.

REFATORAÇÃO DRY: Agora usa HttpErrors para criar exceções HTTP padronizadas.

Responsabilidades:
- Buscar e validar jogadores
- Buscar e validar rotas
- Validar índices de listas
- Validar existência de jogo via GameService
- Lançar HTTPException padronizadas (404, 400)
"""

from typing import List, TYPE_CHECKING
from .http_errors import HttpErrors

if TYPE_CHECKING:
    from ..core.domain.entities.jogo import Jogo
    from ..core.domain.entities.rota import Rota


class GameValidators:
    """Validadores centralizados para entidades do jogo."""
    
    @staticmethod
    def buscar_rota(jogo: 'Jogo', rota_id: str) -> 'Rota':
        """
        Busca rota por ID.
        
        Args:
            jogo: Instância do jogo
            rota_id: ID da rota
            
        Returns:
            Rota encontrada
            
        Raises:
            HTTPException(404): Se rota não existir
        """
        rota = next(
            (r for r in jogo.tabuleiro.rotas if r.id == rota_id),
            None
        )
        
        if not rota:
            raise HttpErrors.not_found("Rota", rota_id)
        
        return rota
    
    @staticmethod
    def validar_indice(
        indice: int,
        tamanho_lista: int,
        nome_campo: str = "item"
    ) -> None:
        """
        Valida se índice está no intervalo [0, tamanho_lista).
        
        Args:
            indice: Índice a validar
            tamanho_lista: Tamanho da lista
            nome_campo: Nome do campo para mensagem de erro
            
        Raises:
            HTTPException(400): Se índice inválido
        """
        if indice < 0 or indice >= tamanho_lista:
            raise HttpErrors.validation_error(
                f"Índice {indice} inválido para {nome_campo}. "
                f"Deve estar entre 0 e {tamanho_lista - 1}",
                field=nome_campo
            )
    
    @staticmethod
    def validar_indices(
        indices: List[int],
        tamanho_lista: int,
        nome_campo: str = "item",
        minimo: int = 1
    ) -> None:
        """
        Valida lista de índices.
        
        Args:
            indices: Lista de índices
            tamanho_lista: Tamanho da lista
            nome_campo: Nome do campo para mensagem de erro
            minimo: Quantidade mínima requerida
            
        Raises:
            HTTPException(400): Se validação falhar
        """
        if not indices:
            raise HttpErrors.validation_error(
                f"Selecione pelo menos {minimo} {nome_campo}(s)",
                field=nome_campo
            )
        
        if len(indices) < minimo:
            raise HttpErrors.validation_error(
                f"Selecione pelo menos {minimo} {nome_campo}(s). "
                f"Foram selecionados apenas {len(indices)}",
                field=nome_campo
            )
        
        indices_unicos = set(indices)
        for indice in indices_unicos:
            GameValidators.validar_indice(indice, tamanho_lista, nome_campo)


