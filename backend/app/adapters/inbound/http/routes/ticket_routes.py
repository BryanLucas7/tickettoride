"""
Rotas relacionadas a bilhetes destino (sorteio, escolha inicial, compra)

Refatoração DRY:
- Usa @auto_save_game para eliminar duplicação de game_service.save_game()
"""

from fastapi import APIRouter, Depends, HTTPException
from .....dependencies import get_ticket_purchase_service
from .....application.services.ticket_purchase_service import TicketPurchaseService
from .....application.services.ticket_selection_service import TicketSelectionService
from .....core.domain.entities.bilhete_destino import BILHETES_DESTINO
from .....shared.formatters import EntityFormatters
from .....shared.exception_handlers import handle_validation_errors
from .....shared.persistence_decorator import auto_save_game
from .....shared.request_context import PlayerRequestContext, get_player_context
from ..schemas import (
    BilheteDestinoResponse,
    ComprarBilhetesRequest,
    BilhetesPendentesResponse,
    EscolherBilhetesIniciaisRequest,
    EscolhaBilhetesIniciaisResponse
)
from random import sample

router = APIRouter()

@router.get("/bilhetes/sortear")
def sortear_bilhetes(quantidade: int = 3):
    """
    Sorteia bilhetes destino aleatórios
    
    Information Expert: BILHETES_DESTINO conhece todos os bilhetes disponíveis
    """
    bilhetes_sorteados = sample(BILHETES_DESTINO, min(quantidade, len(BILHETES_DESTINO)))
    return [
        BilheteDestinoResponse(**EntityFormatters.formatar_bilhete(bilhete))
        for bilhete in bilhetes_sorteados
    ]

@router.get(
    "/{game_id}/players/{player_id}/tickets/initial",
    response_model=BilhetesPendentesResponse
)
def get_initial_tickets(
    ctx: PlayerRequestContext = Depends(get_player_context)
):
    """Retorna os bilhetes iniciais pendentes para o jogador.
    
    Refatoração DRY: Usa PlayerRequestContext para eliminar boilerplate
    """

    bilhetes_pendentes = ctx.jogo.estado.bilhetes_state.obter_pendentes_escolha(ctx.jogador.id)
    if not bilhetes_pendentes:
        raise HTTPException(status_code=404, detail="No pending initial tickets for this player")

    return BilhetesPendentesResponse(
        player_id=str(ctx.jogador.id),
        quantidade_disponivel=len(bilhetes_pendentes),
        minimo_escolha=2,
        maximo_escolha=len(bilhetes_pendentes),
        bilhetes=[
            BilheteDestinoResponse(**EntityFormatters.formatar_bilhete(bilhete))
            for bilhete in bilhetes_pendentes
        ],
    )

@router.post(
    "/{game_id}/players/{player_id}/tickets/initial",
    response_model=EscolhaBilhetesIniciaisResponse
)
@auto_save_game
def escolher_bilhetes_iniciais(
    request: EscolherBilhetesIniciaisRequest,
    ctx: PlayerRequestContext = Depends(get_player_context)
):
    """Confirma a escolha dos bilhetes iniciais de um jogador.
    
    Usa TicketSelectionService (SRP).
    Refatoração DRY:
    - @auto_save_game elimina necessidade de game_service.save_game()
    - PlayerRequestContext elimina boilerplate de parâmetros
    """
    resultado = TicketSelectionService.escolher_bilhetes_iniciais(
        ctx.jogo, ctx.player_id, request.bilhetes_escolhidos, ctx.jogador
    )
    
    if not resultado["success"]:
        raise HTTPException(status_code=400, detail=resultado["message"])
    
    return resultado

@router.post("/{game_id}/players/{player_id}/buy-tickets")
@auto_save_game
@handle_validation_errors
def buy_tickets(
    request: ComprarBilhetesRequest,
    ctx: PlayerRequestContext = Depends(get_player_context),
    purchase_service: TicketPurchaseService = Depends(get_ticket_purchase_service)
):
    """
    Compra bilhetes de destino.
    
    GRASP Controller: API coordena a ação usando TicketPurchaseService
    REGRA: Compra de bilhetes é UMA ação completa - passa turno automaticamente
    Refatoração DRY: PlayerRequestContext elimina boilerplate de parâmetros
    """
    # Converter IDs de bilhetes para índices (0, 1, 2) - decorator trata ValueError
    indices_escolhidos = [int(bid) for bid in request.bilhetes_escolhidos]
    
    # Delegar lógica de compra para o serviço - decorator trata ValueError
    resultado = purchase_service.comprar_bilhetes(
        jogo=ctx.jogo,
        jogador=ctx.jogador,
        indices_escolhidos=indices_escolhidos
    )
    
    return resultado