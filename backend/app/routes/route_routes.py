"""
Rotas relacionadas a rotas do jogo (visualização e conquistas)
"""

from fastapi import APIRouter, HTTPException, Depends
from ..dependencies import get_game_service
from ..services.game_service import GameService
from ..models.entities import Jogo
from ..models.controllers.conquista_rota_controller import ConquistaRotaController
from ..schemas import ConquistarRotaRequest

router = APIRouter()

@router.get("/games/{game_id}/routes")
def get_game_routes(game_id: str, game_service: GameService = Depends(get_game_service)):
    """
    Retorna todas as rotas do jogo com informações de proprietário
    
    Information Expert: Tabuleiro conhece todas as rotas
    """
    jogo = game_service.get_game(game_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Game not found")
    
    routes_data = []
    for rota in jogo.tabuleiro.rotas:
        route_info = {
            "id": rota.id,
            "cidadeA": rota.cidadeA.nome,
            "cidadeB": rota.cidadeB.nome,
            "cor": rota.cor.value,
            "comprimento": rota.comprimento,
            "proprietario_id": rota.proprietario.id if rota.proprietario else None,
            "proprietario_nome": rota.proprietario.nome if rota.proprietario else None,
            "proprietario_cor": rota.proprietario.cor.value if rota.proprietario else None,
            "conquistada": rota.ehConcluida
        }
        routes_data.append(route_info)
    
    return {
        "game_id": game_id,
        "routes": routes_data
    }

@router.post("/games/{game_id}/players/{player_id}/conquer-route")
def conquer_route(game_id: str, player_id: str, request: ConquistarRotaRequest, game_service: GameService = Depends(get_game_service)):
    """
    Conquista uma rota no tabuleiro
    
    GRASP Controller: ConquistaRotaController coordena toda a ação
    REGRA: Conquista de rota é UMA ação completa - passa turno automaticamente
    """
    jogo = game_service.get_game(game_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Game not found")
    
    # Buscar jogador
    jogador = jogo.buscarJogador(player_id)
    if not jogador:
        raise HTTPException(status_code=404, detail="Player not found")
    
    # Buscar rota pelo ID
    rota = next((r for r in jogo.tabuleiro.rotas if r.id == request.rota_id), None)
    if not rota:
        raise HTTPException(status_code=404, detail="Route not found")
    
    # Buscar cartas usadas da mão do jogador
    cartas_em_mao = list(jogador.mao.cartasVagao)
    cartas_usadas = []
    for carta_cor in request.cartas_usadas:
        cor_normalizada = carta_cor.lower()

        indice_encontrado = next(
            (
                idx
                for idx, carta in enumerate(cartas_em_mao)
                if (
                    (carta.ehLocomotiva and cor_normalizada == "locomotiva")
                    or carta.cor.value == cor_normalizada
                )
            ),
            None,
        )

        if indice_encontrado is None:
            raise HTTPException(
                status_code=400,
                detail=f"Card {carta_cor} not found in player's hand",
            )

        cartas_usadas.append(cartas_em_mao.pop(indice_encontrado))
    
    # Importar componentes necessários
    from ..models.managers.descarte_manager import DescarteManager
    from ..models.managers.gerenciador_fim_jogo import GerenciadorFimDeJogo

    descarte_manager = jogo.descarteManager or DescarteManager()

    gerenciador_fim_jogo = jogo.gerenciadorFimDeJogo
    if gerenciador_fim_jogo is None:
        gerenciador_fim_jogo = GerenciadorFimDeJogo(
            total_jogadores=len(jogo.gerenciadorDeTurnos.jogadores)
        )
        jogo.gerenciadorFimDeJogo = gerenciador_fim_jogo
    else:
        gerenciador_fim_jogo.total_jogadores = len(jogo.gerenciadorDeTurnos.jogadores)
    
    # Criar controller e executar conquista
    controller = ConquistaRotaController(
        descarte_manager=descarte_manager,
        validador_duplas=getattr(jogo.tabuleiro, 'validador_duplas', None),
        placar=jogo.placar,
        gerenciador_fim_jogo=gerenciador_fim_jogo
    )
    
    resultado = controller.conquistar_rota(
        jogador=jogador,
        rota=rota,
        cartas_usadas=cartas_usadas,
        total_jogadores=len(jogo.gerenciadorDeTurnos.jogadores)
    )
    
    if not resultado["sucesso"]:
        raise HTTPException(status_code=400, detail=resultado["mensagem"])
    
    # AUTO-PASSAR TURNO: Conquistar rota é uma ação completa
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
    
    game_service.save_game(game_id, jogo)

    return {
        "success": True,
        "message": resultado["mensagem"],
        "points": resultado.get("pontos_ganhos", 0),
        "trains_remaining": resultado.get("trens_restantes", 0),
        "game_ending": resultado.get("fim_de_jogo_ativado", False),
        "turn_completed": True,
        "next_player": jogo.gerenciadorDeTurnos.jogadorAtual,
        "jogo_terminou": jogo_terminou,
        "mensagem_fim": mensagem_fim
    }