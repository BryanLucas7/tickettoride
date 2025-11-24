"""
Contextos de requisição para redução de boilerplate.

GRASP Pattern: Low Coupling, High Cohesion
- Agrega dependências comuns de requisições relacionadas a jogos
- Reduz repetição de parâmetros e Depends() em endpoints
"""
from dataclasses import dataclass
from fastapi import Depends

from ..core.domain.entities.jogo import Jogo
from ..core.domain.entities.jogador import Jogador
from ..application.services.game_service import GameService
from ..dependencies import (
    get_game_service,
    get_validated_game,
    get_validated_player
)


@dataclass
class GameRequestContext:
    """
    Contexto agregado para requisições relacionadas a jogos.
    
    Reduz boilerplate ao encapsular:
    - game_id (path param)
    - jogo validado
    - game_service injetado
    
    Usage:
        @router.get("/games/{game_id}/...")
        def endpoint(ctx: GameRequestContext = Depends()):
            # ctx.game_id, ctx.jogo, ctx.game_service já disponíveis
            ...
    """
    game_id: str
    jogo: Jogo
    game_service: GameService


@dataclass  
class PlayerRequestContext(GameRequestContext):
    """
    Contexto agregado para requisições relacionadas a jogadores.
    
    Herda de GameRequestContext e adiciona:
    - player_id (path param)
    - jogador validado
    
    Usage:
        @router.get("/games/{game_id}/players/{player_id}/...")
        def endpoint(ctx: PlayerRequestContext = Depends()):
            # ctx.game_id, ctx.jogo, ctx.game_service
            # ctx.player_id, ctx.jogador
            ...
    """
    player_id: str
    jogador: Jogador


# ============================================================================
# DEPENDENCY FACTORIES
# ============================================================================

def get_game_context(
    game_id: str,
    jogo: Jogo = Depends(get_validated_game),
    game_service: GameService = Depends(get_game_service)
) -> GameRequestContext:
    """
    Factory para criar GameRequestContext.
    
    FastAPI injeta automaticamente todas as dependências.
    """
    return GameRequestContext(
        game_id=game_id,
        jogo=jogo,
        game_service=game_service
    )


def get_player_context(
    game_id: str,
    player_id: str,
    jogo: Jogo = Depends(get_validated_game),
    jogador: Jogador = Depends(get_validated_player),
    game_service: GameService = Depends(get_game_service)
) -> PlayerRequestContext:
    """
    Factory para criar PlayerRequestContext.
    
    FastAPI injeta automaticamente todas as dependências.
    """
    return PlayerRequestContext(
        game_id=game_id,
        jogo=jogo,
        game_service=game_service,
        player_id=player_id,
        jogador=jogador
    )
