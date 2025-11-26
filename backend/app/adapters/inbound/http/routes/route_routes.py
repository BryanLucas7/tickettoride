"""
Rotas relacionadas a rotas do jogo (visualização e conquistas)

Refatoração DRY:
- Usa @auto_save_game para eliminar duplicação de game_service.save_game()
"""

from fastapi import APIRouter, Depends
from .....dependencies import get_route_conquest_service
from .....application.services.route_conquest_service import RouteConquestService
from .....shared.assemblers import RouteAssembler
from .....shared.persistence_decorator import auto_save_game
from .....shared.request_context import GameRequestContext, PlayerRequestContext, get_game_context, get_player_context
from ..schemas import ConquistarRotaRequest

router = APIRouter()

@router.get("/{game_id}/routes")
def get_game_routes(
    ctx: GameRequestContext = Depends(get_game_context)
):
    """
    Retorna todas as rotas do jogo com informações de proprietário
    
    Information Expert: Tabuleiro conhece todas as rotas
    Refatoração DRY: Usa GameRequestContext para eliminar boilerplate
    """
    # Usar RouteAssembler para montar painel de rotas (migrado de ResponseAssembler)
    painel = RouteAssembler.montar_painel_rotas(ctx.jogo, incluir_proprietario_detalhes=True)
    
    # Ajustar nomes dos campos para resposta esperada
    routes_data = []
    for rota in painel["rotas"]:
        route_info = {
            "id": rota["id"],
            "cidadeA": rota["origem"],
            "cidadeB": rota["destino"],
            "cor": rota["cor"],
            "comprimento": rota["tamanho"],
            "proprietario_id": rota["proprietario"],
            "proprietario_nome": rota.get("proprietario_nome"),
            "proprietario_cor": rota.get("proprietario_cor"),
            "conquistada": rota["conquistada"]
        }
        routes_data.append(route_info)
    
    return {
        "game_id": ctx.game_id,
        "routes": routes_data
    }

@router.post("/{game_id}/players/{player_id}/conquer-route")
@auto_save_game
def conquer_route(
    request: ConquistarRotaRequest,
    ctx: PlayerRequestContext = Depends(get_player_context),
    conquest_service: RouteConquestService = Depends(get_route_conquest_service)
):
    """
    Conquista uma rota no tabuleiro
    
    GRASP Controller: RouteConquestService coordena toda a ação
    REGRA: Conquista de rota é UMA ação completa - passa turno automaticamente
    Refatoração DRY:
    - @auto_save_game elimina necessidade de game_service.save_game()
    - PlayerRequestContext elimina boilerplate de parâmetros
    """
    # Conquistar rota usando o service
    resultado = conquest_service.conquistar_rota(
        jogo=ctx.jogo,
        jogador=ctx.jogador,
        rota_id=request.rota_id,
        cartas_usadas_cores=request.cartas_usadas
    )
    
    return resultado