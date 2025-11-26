"""
Rotas relacionadas a jogadores (cartas, bilhetes, compras)

Refatoração DRY:
- Usa @auto_save_game para eliminar duplicação de game_service.save_game()
"""

from fastapi import APIRouter, Depends, HTTPException
from .....application.services.card_draw_service import CardDrawService
from .....application.services.ticket_preview_service import TicketPreviewService
from .....shared.formatters import EntityFormatters
from .....shared.assemblers import PlayerHandAssembler
from .....shared.persistence_decorator import auto_save_game
from .....shared.request_context import PlayerRequestContext, get_player_context

router = APIRouter()


@router.get("/{game_id}/players/{player_id}/cards")
def get_player_cards(
    ctx: PlayerRequestContext = Depends(get_player_context)
):
    """
    Retorna as cartas de um jogador específico
    
    Information Expert: Jogador conhece suas próprias cartas
    Refatoração DRY: Usa PlayerRequestContext para eliminar boilerplate
    """
    return {
        "player_id": ctx.player_id,
        "cards": EntityFormatters.formatar_cartas(ctx.jogador.cartasVagao)
    }

@router.get("/{game_id}/players/{player_id}/tickets")
def get_player_tickets(
    ctx: PlayerRequestContext = Depends(get_player_context)
):
    """
    Retorna os bilhetes de destino de um jogador específico
    
    Information Expert: Jogador conhece seus próprios bilhetes
    Refatoração DRY: Usa PlayerRequestContext para eliminar boilerplate
    """
    # Usar PlayerHandAssembler para montar mão do jogador (migrado de ResponseAssembler)
    mao = PlayerHandAssembler.montar_mao_completa(
        jogo=ctx.jogo,
        jogador=ctx.jogador,
        incluir_bilhetes=True,
        incluir_cartas=False,
        verificar_bilhetes_completos=True
    )
    
    return {
        "player_id": ctx.player_id,
        "tickets": mao["bilhetes"]
    }

@router.post("/{game_id}/players/{player_id}/tickets/preview")
@auto_save_game
def preview_tickets(
    quantidade: int = 3,
    ctx: PlayerRequestContext = Depends(get_player_context)
):
    """
    Sorteia bilhetes e mantém o conjunto reservado até a confirmação de compra.
    
    Refatoração DRY:
    - Usa TicketPreviewService para lógica de preview
    - @auto_save_game elimina necessidade de save manual
    - PlayerRequestContext elimina boilerplate de parâmetros
    """
    try:
        resultado = TicketPreviewService.preview_bilhetes(ctx.jogo, ctx.player_id, quantidade)
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{game_id}/players/{player_id}/draw-closed")
@auto_save_game
def draw_closed_card(
    ctx: PlayerRequestContext = Depends(get_player_context)
):
    """
    Compra uma carta fechada (do baralho)
    
    Usa CardDrawService (SRP).
    Refatoração DRY:
    - @auto_save_game elimina necessidade de game_service.save_game()
    - PlayerRequestContext elimina boilerplate de parâmetros
    """
    resultado = CardDrawService.comprar_carta_fechada(ctx.jogo, ctx.player_id)
    
    if not resultado["success"]:
        raise HTTPException(status_code=400, detail=resultado["message"])
    
    return resultado

@router.post("/{game_id}/players/{player_id}/draw-open/{card_index}")
@auto_save_game
def draw_open_card(
    card_index: int,
    ctx: PlayerRequestContext = Depends(get_player_context)
):
    """
    Compra uma carta aberta (visível)
    
    Usa CardDrawService (SRP).
    Refatoração DRY:
    - @auto_save_game elimina necessidade de game_service.save_game()
    - PlayerRequestContext elimina boilerplate de parâmetros
    """
    resultado = CardDrawService.comprar_carta_aberta(ctx.jogo, ctx.player_id, card_index)
    
    if not resultado["success"]:
        raise HTTPException(status_code=400, detail=resultado["message"])
    
    return resultado