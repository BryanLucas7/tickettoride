"""
API FastAPI para Ticket to Ride

Implementa os endpoints RESTful para o jogo.

Princípios GRASP aplicados:
- Controller: API endpoints coordenam as ações do jogo
- Pure Fabrication: Schemas Pydantic para camada de API
- Low Coupling: API separada da lógica de domínio
- Indirection: API serve como intermediário entre frontend e backend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import Jogo, Jogador, GerenciadorDeBaralho, Cor
from .models.bilhete_destino import BILHETES_DESTINO
from .models.conquista_rota_controller import ConquistaRotaController
from .models.longest_path import LongestPathCalculator
from .schemas import (
    CreateGameRequest,
    GameResponse,
    GameStateResponse,
    JogadorResponse,
    CartaVagaoResponse,
    MaiorCaminhoLeaderResponse,
    MaiorCaminhoStatusResponse,
    BuyCardsRequest,
    BilheteDestinoResponse,
    ConquistarRotaRequest,
    ComprarBilhetesRequest,
    BilhetesPendentesResponse,
    EscolherBilhetesIniciaisRequest,
    EscolhaBilhetesIniciaisResponse
)
import logging
import pickle
import uuid
from pathlib import Path
from random import sample
from typing import Dict, List, Optional

app = FastAPI(
    title="Ticket to Ride API",
    description="API RESTful para o jogo Ticket to Ride",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://supreme-zebra-6wxrr7g7xx43x4vw-3000.app.github.dev",
        "https://supreme-zebra-6wxrr7g7xx43x4vw-3001.app.github.dev",
        "https://supreme-zebra-6wxrr7g7xx43x4vw-3002.app.github.dev"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (Controller Pattern - coordena o estado do jogo)
active_games: Dict[str, Jogo] = {}

CACHE_FILE = Path(__file__).resolve().parent / ".games_cache.pkl"
LOGGER = logging.getLogger("ticket_to_ride.api")
LONGEST_PATH_CALCULATOR = LongestPathCalculator()


def load_active_games_from_disk() -> None:
    """Carrega jogos ativos do cache em disco, se existir."""
    if not CACHE_FILE.exists():
        return

    try:
        with CACHE_FILE.open("rb") as cache:
            cached_games = pickle.load(cache)

        if isinstance(cached_games, dict):
            active_games.clear()
            active_games.update(cached_games)
            LOGGER.info("Restored %s game(s) from cache", len(active_games))
    except Exception as exc:  # pragma: no cover - logging auxiliar
        LOGGER.warning("Failed to load cached games: %s", exc)


def persist_active_games() -> None:
    """Persiste o estado atual dos jogos para sobreviver a reloads."""
    try:
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with CACHE_FILE.open("wb") as cache:
            pickle.dump(active_games, cache)
    except Exception as exc:  # pragma: no cover - logging auxiliar
        LOGGER.warning("Failed to persist games cache: %s", exc)


load_active_games_from_disk()


def calcular_maior_caminho_status(jogo: Jogo) -> Optional[MaiorCaminhoStatusResponse]:
    """Calcula o status atual do maior caminho contínuo."""
    if not jogo or not jogo.tabuleiro:
        return None

    resultados: List[Dict[str, object]] = []
    for jogador in jogo.gerenciadorDeTurnos.jogadores:
        rotas_jogador = [r for r in jogo.tabuleiro.rotas if r.proprietario == jogador]
        comprimento = 0
        if rotas_jogador:
            comprimento = LONGEST_PATH_CALCULATOR.calcular_maior_caminho(rotas_jogador)

        resultados.append({
            "jogador_id": jogador.id,
            "jogador_nome": jogador.nome,
            "jogador_cor": jogador.cor.value if hasattr(jogador.cor, "value") else jogador.cor,
            "comprimento": comprimento
        })

    if not resultados:
        return None

    maior_comprimento = max(r["comprimento"] for r in resultados)
    lideres = [
        MaiorCaminhoLeaderResponse(
            jogador_id=r["jogador_id"],
            jogador_nome=r["jogador_nome"],
            jogador_cor=r["jogador_cor"]
        )
        for r in resultados
        if r["comprimento"] == maior_comprimento
    ]

    return MaiorCaminhoStatusResponse(
        comprimento=int(maior_comprimento),
        lideres=lideres
    )


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Ticket to Ride API",
        "status": "running",
        "version": "1.0.0",
        "active_games": len(active_games)
    }


@app.post("/games")
async def create_game(request: CreateGameRequest):
    """
    Cria um novo jogo
    
    Controller Pattern: coordena criação do jogo e seus componentes
    """
    # Gera ID único para o jogo
    game_id = f"game-{uuid.uuid4()}"

    # Cria jogo com jogadores
    jogo = Jogo(id=len(active_games))

    numero_jogadores = request.numero_jogadores

    if request.jogadores:
        jogadores_recebidos = request.jogadores
        numero_jogadores = len(jogadores_recebidos)

        cores_usadas = set()
        for indice, jogador_payload in enumerate(jogadores_recebidos):
            nome = jogador_payload.nome.strip()
            cor_payload = jogador_payload.cor.strip()

            try:
                cor_enum = Cor[cor_payload.upper()]
            except KeyError:
                raise HTTPException(status_code=400, detail=f"Cor inválida: {cor_payload}")

            if cor_enum in cores_usadas:
                raise HTTPException(status_code=400, detail=f"Cor duplicada: {cor_enum.value}")
            cores_usadas.add(cor_enum)

            jogador = Jogador(
                id=str(uuid.uuid4()),  # Gera UUID único para cada jogador
                nome=nome,
                cor=cor_enum
            )
            jogo.gerenciadorDeTurnos.adicionarJogador(jogador)
    else:
        cores_padrao = [
            Cor.VERMELHO,
            Cor.AZUL,
            Cor.VERDE,
            Cor.AMARELO,
            Cor.PRETO
        ]

        numero_jogadores = min(numero_jogadores, len(cores_padrao))

        for i in range(numero_jogadores):
            jogador = Jogador(
                id=str(uuid.uuid4()),  # Gera UUID único para cada jogador
                nome=f"Jogador {i+1}",
                cor=cores_padrao[i]
            )
            jogo.gerenciadorDeTurnos.adicionarJogador(jogador)
    
    # Inicializa o jogo
    jogo.iniciar()
    
    # Armazena o jogo
    active_games.clear()
    active_games[game_id] = jogo
    persist_active_games()
    
    # Retorna resposta com jogadores incluídos
    jogadores_response = [
        {
            "id": j.id,
            "nome": j.nome,
            "cor": j.cor.value
        }
        for j in jogo.gerenciadorDeTurnos.jogadores
    ]
    
    return {
        "game_id": game_id,
        "numero_jogadores": len(jogo.gerenciadorDeTurnos.jogadores),
        "iniciado": jogo.iniciado,
        "finalizado": jogo.finalizado,
        "jogadores": jogadores_response
    }


@app.get("/games/{game_id}", response_model=GameStateResponse)
async def get_game_state(game_id: str):
    """
    Retorna o estado atual do jogo
    
    Information Expert: Jogo conhece seu próprio estado
    """
    jogo = active_games.get(game_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Game not found")
    
    # Converte jogadores para response
    jogadores = [
        JogadorResponse(
            id=j.id,
            nome=j.nome,
            cor=j.cor,
            trens_disponiveis=len(j.vagoes),  # Número de vagões disponíveis
            pontos=jogo.placar.obter_pontuacao(j.id) if jogo.placar else 0  # snake_case!
        )
        for j in jogo.gerenciadorDeTurnos.jogadores
    ]
    
    # Converte cartas visíveis
    cartas_visiveis = []
    if jogo.gerenciadorDeBaralho:
        cartas_visiveis = [
            CartaVagaoResponse(cor=carta.cor.value, eh_locomotiva=carta.ehLocomotiva)
            for carta in jogo.gerenciadorDeBaralho.cartasAbertas  # Nome correto!
        ]
    
    maior_caminho_status = calcular_maior_caminho_status(jogo)

    return GameStateResponse(
        game_id=game_id,
        iniciado=jogo.iniciado,
        finalizado=jogo.finalizado,
        jogadores=jogadores,
        jogador_atual_id=jogo.gerenciadorDeTurnos.getJogadorAtual().id if jogo.iniciado else None,  # getJogadorAtual!
        cartas_visiveis=cartas_visiveis,
        maior_caminho=maior_caminho_status
    )


@app.get("/games/{game_id}/players/{player_id}/cards")
async def get_player_cards(game_id: str, player_id: str):
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


@app.get("/games/{game_id}/players/{player_id}/tickets")
async def get_player_tickets(game_id: str, player_id: str):
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


@app.get("/games/{game_id}/routes")
async def get_game_routes(game_id: str):
    """
    Retorna todas as rotas do jogo com informações de proprietário
    
    Information Expert: Tabuleiro conhece todas as rotas
    """
    jogo = active_games.get(game_id)
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


@app.get("/bilhetes/sortear")
async def sortear_bilhetes(quantidade: int = 3):
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


@app.get(
    "/games/{game_id}/players/{player_id}/tickets/initial",
    response_model=BilhetesPendentesResponse
)
async def get_initial_tickets(game_id: str, player_id: str):
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


@app.post(
    "/games/{game_id}/players/{player_id}/tickets/initial",
    response_model=EscolhaBilhetesIniciaisResponse
)
async def escolher_bilhetes_iniciais(
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
        if not bilhete:
            continue
        if bilhete not in bilhetes_aceitos:
            bilhetes_aceitos.append(bilhete)

    if len(bilhetes_aceitos) < 2:
        raise HTTPException(status_code=400, detail="Selection must include at least two valid tickets")

    bilhetes_recusados = [b for b in bilhetes_pendentes if b not in bilhetes_aceitos]

    sucesso = jogo.escolherBilhetesIniciais(jogador.id, ids_recebidos)
    if not sucesso:
        raise HTTPException(status_code=400, detail="Invalid ticket selection")

    persist_active_games()

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


@app.post("/games/{game_id}/players/{player_id}/tickets/preview")
async def preview_tickets(game_id: str, player_id: str, quantidade: int = 3):
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

    persist_active_games()

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


@app.post("/games/{game_id}/players/{player_id}/draw-closed")
async def draw_closed_card(game_id: str, player_id: str):
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
    persist_active_games()

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


@app.post("/games/{game_id}/players/{player_id}/draw-open/{card_index}")
async def draw_open_card(game_id: str, player_id: str, card_index: int):
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
    persist_active_games()

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


@app.post("/games/{game_id}/players/{player_id}/conquer-route")
async def conquer_route(game_id: str, player_id: str, request: ConquistarRotaRequest):
    """
    Conquista uma rota no tabuleiro
    
    GRASP Controller: ConquistaRotaController coordena toda a ação
    REGRA: Conquista de rota é UMA ação completa - passa turno automaticamente
    """
    jogo = active_games.get(game_id)
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
    from .models.descarte_manager import DescarteManager
    from .models.gerenciador_fim_jogo import GerenciadorFimDeJogo

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
    
    persist_active_games()

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


@app.post("/games/{game_id}/players/{player_id}/buy-tickets")
async def buy_tickets(game_id: str, player_id: str, request: ComprarBilhetesRequest):
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
    
    persist_active_games()

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


@app.post("/games/{game_id}/next-turn")
async def next_turn(game_id: str):
    """
    Passa para o próximo turno
    """
    jogo = active_games.get(game_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Game not found")
    
    # Avança turno
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
    
    persist_active_games()

    return {
        "success": True,
        "current_player": jogo.gerenciadorDeTurnos.jogadorAtual,
        "message": f"Turno passado para jogador {jogo.gerenciadorDeTurnos.jogadorAtual}",
        "jogo_terminou": jogo_terminou,
        "mensagem_fim": mensagem_fim
    }


@app.get("/games/{game_id}/pontuacao-final")
async def get_pontuacao_final(game_id: str):
    """
    CORREÇÃO BUG #3: Endpoint para calcular e retornar pontuação final
    
    Calcula pontuação final de todos os jogadores e determina vencedor(es).
    Deve ser chamado quando jogo.finalizado == True.
    
    Returns:
        - pontuacoes: Array com pontuação detalhada de cada jogador
        - vencedor: ID do vencedor ou lista de IDs se empate
        - mensagem: Mensagem de resultado
    """
    jogo = active_games.get(game_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Game not found")
    
    if not jogo.finalizado:
        raise HTTPException(status_code=400, detail="Game not finished yet")
    
    # Importar componentes necessários
    from .models.pontuacao_final import PontuacaoFinalCalculator
    from .models.pathfinder import VerificadorBilhetes
    from .models.longest_path import LongestPathCalculator
    
    # Instanciar calculadores
    verificador = VerificadorBilhetes()
    longest_path_calc = LongestPathCalculator()
    calculator = PontuacaoFinalCalculator(
        verificador_bilhetes=verificador,
        longest_path_calculator=longest_path_calc
    )
    
    # Calcular pontuações de todos os jogadores
    resultados = {}
    
    for jogador in jogo.gerenciadorDeTurnos.jogadores:
        # Obter rotas conquistadas pelo jogador
        rotas_jogador = [r for r in jogo.tabuleiro.rotas if r.proprietario == jogador]
        
        # Calcular pontuação
        resultado = calculator.calcular_pontuacao_jogador(
            jogador_id=jogador.id,
            pontos_rotas=jogo.placar.obter_pontuacao(jogador.id) if jogo.placar else 0,
            bilhetes=jogador.bilhetes,
            rotas_conquistadas=rotas_jogador
        )
        
        resultados[jogador.id] = resultado
    
    # Determinar jogadores com maior caminho
    maior_comprimento = 0
    for resultado in resultados.values():
        if resultado.comprimento_maior_caminho > maior_comprimento:
            maior_comprimento = resultado.comprimento_maior_caminho
    
    # Aplicar bônus de +10 para jogadores com maior caminho
    for resultado in resultados.values():
        if resultado.comprimento_maior_caminho == maior_comprimento and maior_comprimento > 0:
            resultado.bonus_maior_caminho = 10
            resultado.pontuacao_total += 10
        else:
            resultado.bonus_maior_caminho = 0
    
    # Determinar vencedor(es) com critérios de desempate
    jogadores_ordenados = sorted(
        resultados.items(),
        key=lambda x: (
            x[1].pontuacao_total,
            x[1].bilhetes_completos,
            x[1].comprimento_maior_caminho
        ),
        reverse=True
    )
    
    vencedor_id, vencedor_resultado = jogadores_ordenados[0]
    
    # Verificar empates
    empatados = [vencedor_id]
    for jogador_id, resultado in jogadores_ordenados[1:]:
        if (
            resultado.pontuacao_total == vencedor_resultado.pontuacao_total and
            resultado.bilhetes_completos == vencedor_resultado.bilhetes_completos and
            resultado.comprimento_maior_caminho == vencedor_resultado.comprimento_maior_caminho
        ):
            empatados.append(jogador_id)
        else:
            break
    
    vencedor = empatados[0] if len(empatados) == 1 else empatados
    
    # Converter resultados para JSON
    pontuacoes = []
    for jogador_id, resultado in resultados.items():
        jogador = jogo.buscarJogador(jogador_id)
        
        pontuacoes.append({
            "jogador_id": jogador_id,
            "jogador_nome": jogador.nome if jogador else f"Jogador {jogador_id}",
            "jogador_cor": jogador.cor.value if jogador else "unknown",
            "pontos_rotas": resultado.pontos_rotas,
            "bilhetes_completos": [
                {
                    "origem": b.cidadeOrigem.nome,
                    "destino": b.cidadeDestino.nome,
                    "pontos": b.pontos,
                    "completo": True
                }
                for b in resultado.bilhetes_completos_lista
            ],
            "bilhetes_incompletos": [
                {
                    "origem": b.cidadeOrigem.nome,
                    "destino": b.cidadeDestino.nome,
                    "pontos": b.pontos,
                    "completo": False
                }
                for b in resultado.bilhetes_incompletos_lista
            ],
            "pontos_bilhetes_positivos": resultado.pontos_bilhetes_completos,
            "pontos_bilhetes_negativos": resultado.pontos_bilhetes_incompletos,
            "bonus_maior_caminho": resultado.bonus_maior_caminho > 0,
            "pontos_maior_caminho": resultado.bonus_maior_caminho,
            "pontuacao_total": resultado.pontuacao_total,
            "tamanho_maior_caminho": resultado.comprimento_maior_caminho
        })
    
    # Ordenar por pontuação (maior primeiro)
    pontuacoes.sort(key=lambda p: p["pontuacao_total"], reverse=True)
    
    # Criar mensagem de vencedor
    if isinstance(vencedor, list):
        nomes = [jogo.buscarJogador(v).nome for v in vencedor]
        mensagem = f"Empate! Vencedores: {', '.join(nomes)}"
    else:
        jogador_vencedor = jogo.buscarJogador(vencedor)
        mensagem = f"{jogador_vencedor.nome} venceu o jogo!"
    
    return {
        "success": True,
        "pontuacoes": pontuacoes,
        "vencedor": vencedor,
        "mensagem": mensagem
    }
