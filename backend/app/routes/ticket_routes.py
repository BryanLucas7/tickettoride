"""
Rotas relacionadas a bilhetes destino (sorteio, escolha inicial, compra)
"""

from fastapi import APIRouter, HTTPException
from ..models.entities import Jogo
from ..models.entities.bilhete_destino import BILHETES_DESTINO
from ..schemas import (
    BilheteDestinoResponse,
    ComprarBilhetesRequest,
    BilhetesPendentesResponse,
    EscolherBilhetesIniciaisRequest,
    EscolhaBilhetesIniciaisResponse
)
from random import sample
from typing import Dict

router = APIRouter()

# Referência ao dicionário global
from .game_routes import active_games

@router.get("/bilhetes/sortear")
def sortear_bilhetes(quantidade: int = 3):
    """
    Sorteia bilhetes destino aleatórios
    
    Information Expert: BILHETES_DESTINO conhece todos os bilhetes disponíveis
    """
    bilhetes_sorteados = sample(BILHETES_DESTINO, min(quantidade, len(BILHETES_DESTINO)))
    return [
        BilheteDestinoResponse(
            id=bilhete.id,
            cidadeOrigem=bilhete.cidadeOrigem.nome,
            cidadeDestino=bilhete.cidadeDestino.nome,
            pontos=bilhete.pontos
        )
        for bilhete in bilhetes_sorteados
    ]

@router.get(
    "/games/{game_id}/players/{player_id}/tickets/initial",
    response_model=BilhetesPendentesResponse
)
def get_initial_tickets(game_id: str, player_id: str):
    """Retorna os bilhetes iniciais pendentes para o jogador."""

    jogo = active_games.get(game_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Game not found")

    jogador = jogo.buscarJogador(player_id)
    if not jogador:
        raise HTTPException(status_code=404, detail="Player not found")

    bilhetes_pendentes = jogo.bilhetesPendentesEscolha.get(jogador.id)
    if not bilhetes_pendentes:
        raise HTTPException(status_code=404, detail="No pending initial tickets for this player")

    return BilhetesPendentesResponse(
        player_id=str(jogador.id),
        quantidade_disponivel=len(bilhetes_pendentes),
        minimo_escolha=2,
        maximo_escolha=len(bilhetes_pendentes),
        bilhetes=[
            BilheteDestinoResponse(
                id=bilhete.id,
                cidadeOrigem=bilhete.cidadeOrigem.nome,
                cidadeDestino=bilhete.cidadeDestino.nome,
                pontos=bilhete.pontos,
            )
            for bilhete in bilhetes_pendentes
        ],
    )

@router.post(
    "/games/{game_id}/players/{player_id}/tickets/initial",
    response_model=EscolhaBilhetesIniciaisResponse
)
def escolher_bilhetes_iniciais(
    game_id: str,
    player_id: str,
    request: EscolherBilhetesIniciaisRequest,
):
    """Confirma a escolha dos bilhetes iniciais de um jogador."""

    jogo = active_games.get(game_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Game not found")

    jogador = jogo.buscarJogador(player_id)
    if not jogador:
        raise HTTPException(status_code=404, detail="Player not found")

    bilhetes_pendentes = jogo.bilhetesPendentesEscolha.get(jogador.id)
    if not bilhetes_pendentes:
        raise HTTPException(status_code=400, detail="No pending initial ticket selection for this player")

    ids_recebidos = list(request.bilhetes_escolhidos)
    if len(ids_recebidos) < 2:
        raise HTTPException(status_code=400, detail="Select at least two tickets")
    if len(ids_recebidos) > len(bilhetes_pendentes):
        raise HTTPException(status_code=400, detail="Cannot select more tickets than available")

    def resolver_bilhete(identificador):
        for bilhete in bilhetes_pendentes:
            if bilhete.id == identificador:
                return bilhete
            try:
                if id(bilhete) == int(identificador):
                    return bilhete
            except (TypeError, ValueError):
                continue
        return None

    bilhetes_aceitos = []
    for identificador in ids_recebidos:
        bilhete = resolver_bilhete(identificador)
        if bilhete:
            if bilhete not in bilhetes_aceitos:
                bilhetes_aceitos.append(bilhete)

    if len(bilhetes_aceitos) < 2:
        raise HTTPException(status_code=400, detail="Selection must include at least two valid tickets")

    bilhetes_recusados = [b for b in bilhetes_pendentes if b not in bilhetes_aceitos]

    sucesso = jogo.escolherBilhetesIniciais(jogador.id, ids_recebidos)
    if not sucesso:
        raise HTTPException(status_code=400, detail="Invalid ticket selection")

    # persist_active_games()  # Removido

    return EscolhaBilhetesIniciaisResponse(
        success=True,
        player_id=str(jogador.id),
        tickets_kept=len(bilhetes_aceitos),
        tickets_returned=len(bilhetes_recusados),
        bilhetes=[
            BilheteDestinoResponse(
                id=bilhete.id,
                cidadeOrigem=bilhete.cidadeOrigem.nome,
                cidadeDestino=bilhete.cidadeDestino.nome,
                pontos=bilhete.pontos,
            )
            for bilhete in bilhetes_aceitos
        ],
    )

@router.post("/games/{game_id}/players/{player_id}/buy-tickets")
def buy_tickets(game_id: str, player_id: str, request: ComprarBilhetesRequest):
    """
    Compra bilhetes de destino
    
    GRASP Controller: API coordena a ação reutilizando bilhetes reservados
    REGRA: Compra de bilhetes é UMA ação completa - passa turno automaticamente
    """
    jogo = active_games.get(game_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Game not found")
    
    # Buscar jogador
    jogador = jogo.buscarJogador(player_id)
    if not jogador:
        raise HTTPException(status_code=404, detail="Player not found")
    
    bilhetes_reservados = jogo.bilhetesPendentesCompra.get(player_id)
    if not bilhetes_reservados:
        raise HTTPException(status_code=400, detail="No pending ticket selection for this player")

    # Converter IDs de bilhetes para índices (0, 1, 2)
    try:
        indices_escolhidos = [int(bid) for bid in request.bilhetes_escolhidos]
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid ticket IDs format")
    
    if not indices_escolhidos:
        raise HTTPException(status_code=400, detail="Select at least one ticket")

    total_disponivel = len(bilhetes_reservados)
    indices_unicos = sorted(set(indices_escolhidos))

    if any(indice < 0 or indice >= total_disponivel for indice in indices_unicos):
        raise HTTPException(status_code=400, detail="Invalid ticket indices")

    bilhetes_escolhidos = [bilhetes_reservados[indice] for indice in indices_unicos]
    bilhetes_recusados = [
        bilhete
        for indice, bilhete in enumerate(bilhetes_reservados)
        if indice not in indices_unicos
    ]

    # Persistir escolha do jogador
    jogador.bilhetes.extend(bilhetes_escolhidos)

    if bilhetes_recusados:
        jogo.gerenciadorDeBaralho.devolverBilhetes(bilhetes_recusados)

    # Limpa reserva para permitir novas compras futuras
    jogo.bilhetesPendentesCompra.pop(player_id, None)

    quantidade_escolhidos = len(bilhetes_escolhidos)
    quantidade_recusados = len(bilhetes_recusados)

    destino_texto = ", ".join(
        f"{bilhete.cidadeOrigem.nome} → {bilhete.cidadeDestino.nome}"
        for bilhete in bilhetes_escolhidos
    )

    mensagem = (
        f"{jogador.nome} ficou com {quantidade_escolhidos} bilhete(s)"
        f" e devolveu {quantidade_recusados}."
    )
    if destino_texto:
        mensagem += f" Bilhetes escolhidos: {destino_texto}."

    resultado = {
        "sucesso": True,
        "mensagem": mensagem,
        "quantidade_escolhidos": quantidade_escolhidos,
        "quantidade_recusados": quantidade_recusados,
    }
    
    # AUTO-PASSAR TURNO: Compra de bilhetes é uma ação completa
    jogo.estadoCompraCartas.resetar()  # Reseta estado de compra para próximo turno
    jogo.gerenciadorDeTurnos.nextTurn()
    
    # CORREÇÃO BUG #1: Processar turno na última rodada
    jogo_terminou = False
    mensagem_fim = None
    if jogo.gerenciadorFimDeJogo and jogo.gerenciadorFimDeJogo.ultima_rodada_ativada:
        resultado_fim = jogo.gerenciadorFimDeJogo.processar_turno_jogado()
        if resultado_fim["jogo_terminou"]:
            jogo.encerrar()
            jogo_terminou = True
            mensagem_fim = resultado_fim["mensagem"]
    
    # persist_active_games()  # Removido

    return {
        "success": True,
        "message": resultado["mensagem"],
        "tickets_kept": resultado.get("quantidade_escolhidos", 0),
        "tickets_returned": resultado.get("quantidade_recusados", 0),
        "turn_completed": True,
        "next_player": jogo.gerenciadorDeTurnos.jogadorAtual,
        "jogo_terminou": jogo_terminou,
        "mensagem_fim": mensagem_fim
    }