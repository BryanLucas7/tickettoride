"""
Rotas relacionadas a jogadores (cartas, bilhetes, compras)
"""

from fastapi import APIRouter, HTTPException, Depends
from ..dependencies import get_game_service
from ..services.game_service import GameService
from ..models.entities import Jogo
from ..models.entities.bilhete_destino import BILHETES_DESTINO
from ..schemas import (
    CartaVagaoResponse,
    BilheteDestinoResponse,
    ComprarBilhetesRequest,
    BilhetesPendentesResponse,
    EscolherBilhetesIniciaisRequest,
    EscolhaBilhetesIniciaisResponse
)
import logging
from typing import Dict

router = APIRouter()


@router.get("/games/{game_id}/players/{player_id}/cards")
def get_player_cards(game_id: str, player_id: str):
    """
    Retorna as cartas de um jogador específico
    
    Information Expert: Jogador conhece suas próprias cartas
    """
    jogo = active_games.get(game_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Game not found")
    
    jogador = jogo.buscarJogador(player_id)
    if not jogador:
        raise HTTPException(status_code=404, detail="Player not found")
    
    return {
        "player_id": player_id,
        "cards": [
            {"cor": carta.cor.value, "eh_locomotiva": carta.ehLocomotiva}
            for carta in jogador.cartasVagao
        ]  # Backend envia lowercase
    }

@router.get("/games/{game_id}/players/{player_id}/tickets")
def get_player_tickets(game_id: str, player_id: str):
    """
    Retorna os bilhetes de destino de um jogador específico
    
    Information Expert: Jogador conhece seus próprios bilhetes
    """
    jogo = active_games.get(game_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Game not found")
    
    jogador = jogo.buscarJogador(player_id)
    if not jogador:
        raise HTTPException(status_code=404, detail="Player not found")
    
    # Verifica quais bilhetes foram completados usando o pathfinder
    bilhetes_com_status = []
    
    # Obter rotas conquistadas pelo jogador
    rotas_jogador = [r for r in jogo.tabuleiro.rotas if r.proprietario == jogador]
    
    for bilhete in jogador.bilhetes:
        completo = False
        if jogo.pathfinder:
            completo = jogo.pathfinder.verificar_bilhete_completo(
                bilhete=bilhete,
                rotas_conquistadas=rotas_jogador
            )
        
        bilhetes_com_status.append({
            "id": bilhete.id,
            "cidadeOrigem": bilhete.cidadeOrigem.nome,
            "cidadeDestino": bilhete.cidadeDestino.nome,
            "pontos": bilhete.pontos,
            "completo": completo
        })
    
    return {
        "player_id": player_id,
        "tickets": bilhetes_com_status
    }

@router.post("/games/{game_id}/players/{player_id}/tickets/preview")
def preview_tickets(game_id: str, player_id: str, quantidade: int = 3):
    """
    Sorteia bilhetes e mantém o conjunto reservado até a confirmação de compra.
    """
    if quantidade < 1 or quantidade > 3:
        raise HTTPException(status_code=400, detail="Quantity must be between 1 and 3")

    jogo = active_games.get(game_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Game not found")

    jogador = jogo.buscarJogador(player_id)
    if not jogador:
        raise HTTPException(status_code=404, detail="Player not found")

    if not jogo.gerenciadorDeBaralho:
        raise HTTPException(status_code=500, detail="Deck not initialized")

    bilhetes_reservados = jogo.bilhetesPendentesCompra.get(player_id)

    if not bilhetes_reservados:
        cartas_disponiveis = jogo.gerenciadorDeBaralho.baralhoBilhetes.cartas
        if not cartas_disponiveis:
            raise HTTPException(status_code=400, detail="No tickets available")

        quantidade_real = min(quantidade, len(cartas_disponiveis))
        bilhetes_reservados = []

        for _ in range(quantidade_real):
            bilhete = jogo.gerenciadorDeBaralho.baralhoBilhetes.comprar()
            if bilhete:
                bilhetes_reservados.append(bilhete)

        if not bilhetes_reservados:
            raise HTTPException(status_code=400, detail="No tickets available")

        jogo.bilhetesPendentesCompra[player_id] = bilhetes_reservados

    # persist_active_games()  # Removido

    return {
        "tickets": [
            {
                "index": indice,
                "id": bilhete.id,
                "origem": bilhete.cidadeOrigem.nome,
                "destino": bilhete.cidadeDestino.nome,
                "pontos": bilhete.pontos,
            }
            for indice, bilhete in enumerate(bilhetes_reservados)
        ],
        "quantidade": len(bilhetes_reservados),
    }

@router.post("/games/{game_id}/players/{player_id}/draw-closed")
def draw_closed_card(game_id: str, player_id: str):
    """
    Compra uma carta fechada (do baralho)
    
    REGRA: Se completar o turno (2 cartas), passa automaticamente
    """
    jogo = active_games.get(game_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Game not found")
    
    resultado = jogo.comprarCartaDoBaralhoFechado(player_id)
    
    if not resultado["sucesso"]:
        raise HTTPException(status_code=400, detail=resultado["mensagem"])
    
    # AUTO-PASSAR TURNO: Se completar o turno (2 cartas), passa automaticamente
    turno_completo = jogo.estadoCompraCartas.turnoCompleto
    if turno_completo:
        jogo.estadoCompraCartas.resetar()
        jogo.gerenciadorDeTurnos.nextTurn()
        
        # CORREÇÃO BUG #1: Processar turno na última rodada
        if jogo.gerenciadorFimDeJogo and jogo.gerenciadorFimDeJogo.ultima_rodada_ativada:
            resultado_fim = jogo.gerenciadorFimDeJogo.processar_turno_jogado()
            if resultado_fim["jogo_terminou"]:
                jogo.encerrar()
                resultado["jogo_terminou"] = True
                resultado["mensagem_fim"] = resultado_fim["mensagem"]
        
        resultado["turno_passado"] = True
        resultado["proximo_jogador"] = jogo.gerenciadorDeTurnos.jogadorAtual
    else:
        resultado["turno_passado"] = False
    
    carta = resultado.get("carta") or {}
    # persist_active_games()  # Removido

    return {
        "success": True,
        "message": resultado["mensagem"],
        "card": {
            "cor": carta.get("cor", ""),
            "eh_locomotiva": carta.get("ehLocomotiva", False)
        },
        "turn_completed": turno_completo,
        "next_player": resultado.get("proximo_jogador")
    }

@router.post("/games/{game_id}/players/{player_id}/draw-open/{card_index}")
def draw_open_card(game_id: str, player_id: str, card_index: int):
    """
    Compra uma carta aberta (visível)
    
    REGRA: Se comprar locomotiva ou completar 2 cartas, passa automaticamente
    """
    jogo = active_games.get(game_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Game not found")
    
    resultado = jogo.comprarCartaAberta(player_id, card_index)
    
    if not resultado["sucesso"]:
        raise HTTPException(status_code=400, detail=resultado["mensagem"])
    
    # AUTO-PASSAR TURNO: Se completou a ação de compra
    turno_completo = jogo.estadoCompraCartas.turnoCompleto
    if turno_completo:
        jogo.estadoCompraCartas.resetar()
        jogo.gerenciadorDeTurnos.nextTurn()
        
        # CORREÇÃO BUG #1: Processar turno na última rodada
        if jogo.gerenciadorFimDeJogo and jogo.gerenciadorFimDeJogo.ultima_rodada_ativada:
            resultado_fim = jogo.gerenciadorFimDeJogo.processar_turno_jogado()
            if resultado_fim["jogo_terminou"]:
                jogo.encerrar()
                resultado["jogo_terminou"] = True
                resultado["mensagem_fim"] = resultado_fim["mensagem"]
        
        resultado["turno_passado"] = True
        resultado["proximo_jogador"] = jogo.gerenciadorDeTurnos.jogadorAtual
    else:
        resultado["turno_passado"] = False
    
    carta = resultado.get("carta") or {}
    # persist_active_games()  # Removido

    return {
        "success": True,
        "message": resultado["mensagem"],
        "card": {
            "cor": carta.get("cor", ""),
            "eh_locomotiva": carta.get("ehLocomotiva", False)
        },
        "turn_completed": turno_completo,
        "next_player": resultado.get("proximo_jogador")
    }

@router.post("/games/{game_id}/players/{player_id}/tickets/preview", response_model=BilhetesPendentesResponse)
def preview_tickets(game_id: str, player_id: str):
    """Mostra preview de bilhetes para o jogador escolher"""
    jogo = game_service.get_game(game_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")

    jogador = next((p for p in jogo.jogadores if p.id == player_id), None)
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")

    # Lógica de preview (simplificada)
    bilhetes_sorteados = sample(BILHETES_DESTINO, 3)
    return BilhetesPendentesResponse(
        bilhetes=[b.to_dict() for b in bilhetes_sorteados]
    )

@router.post("/games/{game_id}/players/{player_id}/draw-closed")
def draw_closed_card(game_id: str, player_id: str):
    """Compra uma carta fechada"""
    jogo = game_service.get_game(game_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")

    jogador = next((p for p in jogo.jogadores if p.id == player_id), None)
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")

    try:
        carta = jogo.baralho.comprar_carta_fechada()
        jogador.mao.adicionar_carta(carta)
        game_service.save_game(game_id)
        return {"message": "Carta comprada", "card": carta.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/games/{game_id}/players/{player_id}/draw-open/{card_index}")
def draw_open_card(game_id: str, player_id: str, card_index: int):
    """Compra uma carta aberta"""
    jogo = game_service.get_game(game_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")

    jogador = next((p for p in jogo.jogadores if p.id == player_id), None)
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")

    try:
        carta = jogo.baralho.comprar_carta_aberta(card_index)
        jogador.mao.adicionar_carta(carta)
        game_service.save_game(game_id)
        return {"message": "Carta aberta comprada", "card": carta.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/games/{game_id}/players/{player_id}/buy-tickets")
def buy_tickets(game_id: str, player_id: str, request: ComprarBilhetesRequest):
    """Compra bilhetes destino"""
    jogo = game_service.get_game(game_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")

    jogador = next((p for p in jogo.jogadores if p.id == player_id), None)
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")

    try:
        # Lógica simplificada
        for bilhete_id in request.bilhete_ids:
            bilhete = next((b for b in BILHETES_DESTINO if b.id == bilhete_id), None)
            if bilhete:
                jogador.adicionar_bilhete(bilhete)
        game_service.save_game(game_id)
        return {"message": "Bilhetes comprados"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))