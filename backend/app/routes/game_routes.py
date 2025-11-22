"""
Rotas relacionadas a jogos (criação, estado, turnos, pontuação)
"""

from fastapi import APIRouter, HTTPException, Depends
from ..models.entities import Jogo, Jogador, Cor
from ..schemas import (
    CreateGameRequest,
    GameResponse,
    GameStateResponse,
    JogadorResponse,
    CartaVagaoResponse,
    MaiorCaminhoLeaderResponse,
    MaiorCaminhoStatusResponse,
    EscolherBilhetesIniciaisRequest,
    EscolhaBilhetesIniciaisResponse
)
import logging
import uuid
from typing import Dict, List, Optional
from ..dependencies import get_game_service
from ..services.game_service import GameService

router = APIRouter()



def calcular_maior_caminho_status(jogo: Jogo) -> Optional[MaiorCaminhoStatusResponse]:
    """Calcula o status atual do maior caminho contínuo."""
    from ..models.calculators.longest_path import LongestPathCalculator
    LONGEST_PATH_CALCULATOR = LongestPathCalculator()
    
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

@router.get("/")
def read_root():
    """Endpoint raiz da API"""
    return {"message": "Ticket to Ride API", "version": "1.0.0"}

@router.post("/games", response_model=GameResponse)
def create_game(request: CreateGameRequest, game_service: GameService = Depends(get_game_service)):
    """
    Cria um novo jogo
    
    Controller Pattern: coordena criação do jogo e seus componentes
    """
    # Gera ID único para o jogo
    game_id = f"game-{uuid.uuid4()}"

    # Cria jogo com jogadores
    jogo = Jogo(id=game_id)

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
    game_service.save_game(game_id, jogo)
    
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

@router.get("/games/{game_id}", response_model=GameStateResponse)
def get_game_state(game_id: str, game_service: GameService = Depends(get_game_service)):
    """
    Retorna o estado atual do jogo
    
    Information Expert: Jogo conhece seu próprio estado
    """
    jogo = game_service.get_game(game_id)
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

@router.post("/games/{game_id}/next-turn")
def next_turn(game_id: str, game_service: GameService = Depends(get_game_service)):
    """
    Passa para o próximo turno
    """
    jogo = game_service.get_game(game_id)
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
    
    game_service.save_game(game_id, jogo)

    return {
        "success": True,
        "current_player": jogo.gerenciadorDeTurnos.jogadorAtual,
        "message": f"Turno passado para jogador {jogo.gerenciadorDeTurnos.jogadorAtual}",
        "jogo_terminou": jogo_terminou,
        "mensagem_fim": mensagem_fim
    }

@router.get("/games/{game_id}/pontuacao-final")
def get_pontuacao_final(game_id: str, game_service: GameService = Depends(get_game_service)):
    """
    CORREÇÃO BUG #3: Endpoint para calcular e retornar pontuação final
    
    Calcula pontuação final de todos os jogadores e determina vencedor(es).
    Deve ser chamado quando jogo.finalizado == True.
    
    Returns:
        - pontuacoes: Array com pontuação detalhada de cada jogador
        - vencedor: ID do vencedor ou lista de IDs se empate
        - mensagem: Mensagem de resultado
    """
    jogo = game_service.get_game(game_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Game not found")
    
    if not jogo.finalizado:
        raise HTTPException(status_code=400, detail="Game not finished yet")
    
    # Importar componentes necessários
    from ..models.calculators.pontuacao_final_calculator import PontuacaoFinalCalculator
    from ..models.calculators.verificador_bilhetes import VerificadorBilhetes
    from ..models.calculators.longest_path import LongestPathCalculator
    
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

