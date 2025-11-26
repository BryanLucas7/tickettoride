"""
Dependências de Validação para FastAPI.

Padrão GRASP: Controller (coordena validação)
Padrão GoF: Strategy (validações são intercambiáveis)

REFATORAÇÃO DRY: Agora usa HttpErrors para criar exceções HTTP padronizadas.

Este módulo fornece dependências que validam entidades do jogo
antes de processá-las nos endpoints.

Substitui padrões antigos (REMOVIDOS):
- decorators/validation.py (@require_game, @require_game_and_player)  
- utils/validation_helpers.py (validate_game, validate_game_and_player)
- GameValidators.validar_jogo_existe() e validar_jogo_e_jogador()

Uso idiomático com FastAPI Depends():

    @router.get("/games/{game_id}/...")
    def endpoint(
        game_id: str,
        jogo: Jogo = Depends(get_validated_game)
    ):
        # jogo já está validado e pronto para uso
        ...

    @router.get("/games/{game_id}/players/{player_id}/...")
    def endpoint(
        game_id: str,
        player_id: str,
        jogador: Jogador = Depends(get_validated_player),
        jogo: Jogo = Depends(get_validated_game)  # opcional
    ):
        # jogador e jogo validados
        ...
"""

import logging
from fastapi import Depends

from ..core.domain.entities.jogo import Jogo
from ..core.domain.entities.jogador import Jogador
from ..application.services.game_service import GameService
from ..shared.http_errors import HttpErrors
from .services import get_game_service

logger = logging.getLogger(__name__)


def get_validated_game(
    game_id: str,
    game_service: GameService = Depends(get_game_service)
) -> Jogo:
    """
    Valida e retorna o jogo.
    
    GRASP Controller: Coordena validação de jogo via GameService.
    Substitui padrão duplicado em múltiplos lugares do código.
    
    REFATORAÇÃO DRY: Usa HttpErrors para exceções padronizadas.
    
    Args:
        game_id: ID do jogo
        game_service: Service injetado automaticamente
        
    Returns:
        Jogo validado
        
    Raises:
        HTTPException(404): Se jogo não existir
        
    Usage:
        @router.get("/games/{game_id}/state")
        def get_state(
            game_id: str,
            jogo: Jogo = Depends(get_validated_game)
        ):
            return {"state": jogo.estado.iniciado}
    """
    jogo = game_service.get_game(game_id)
    if not jogo:
        raise HttpErrors.not_found("Game", game_id)
    return jogo


def get_validated_player(
    game_id: str,
    player_id: str,
    jogo: Jogo = Depends(get_validated_game)
) -> Jogador:
    """
    Valida e retorna o jogador. Já inclui validação do jogo.
    
    GRASP Controller: Coordena validação de jogador.
    Information Expert: Usa GerenciadorDeTurnos.obter_jogador_por_id().
    
    REFATORAÇÃO DRY: Usa HttpErrors para exceções padronizadas.
    
    Args:
        game_id: ID do jogo (usado para validar jogo primeiro)
        player_id: ID do jogador
        jogo: Jogo já validado (injetado automaticamente)
        
    Returns:
        Jogador validado
        
    Raises:
        HTTPException(404): Se jogador não existir
        
    Usage:
        @router.get("/games/{game_id}/players/{player_id}/cards")
        def get_cards(
            game_id: str,
            player_id: str,
            jogador: Jogador = Depends(get_validated_player)
        ):
            return {"cards": jogador.mao.cartasVagao}
    """
    jogador = jogo.gerenciadorDeTurnos.obter_jogador_por_id(player_id)
    if not jogador:
        raise HttpErrors.not_found("Player", player_id)
    
    return jogador
