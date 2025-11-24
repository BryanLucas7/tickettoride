"""
Rotas relacionadas a jogos (criação, estado, turnos, pontuação)

Refatoração DRY:
- Usa @auto_save_game para eliminar duplicação de game_service.save_game()
"""

from fastapi import APIRouter, Depends
from ..schemas import (
    CreateGameRequest,
    GameResponse,
    GameStateResponse,
    JogadorResponse,
    CartaVagaoResponse
)
from .....dependencies import (
    get_game_service, 
    get_game_action_service, 
    get_game_creation_service, 
    get_pontuacao_final_service, 
    get_longest_path_service
)
from .....shared.response_assembler import ResponseAssembler
from .....shared.persistence_decorator import auto_save_game
from .....shared.request_context import GameRequestContext, get_game_context
from .....application.services.game_service import GameService
from .....application.services.game_action_service import GameActionService
from .....application.services.game_creation_service import GameCreationService
from .....application.services.pontuacao_final_service import PontuacaoFinalService
from .....application.services.longest_path_service import LongestPathService

router = APIRouter()


@router.get("/")
def read_root():
    """Endpoint raiz da API"""
    return {"message": "Ticket to Ride API", "version": "1.0.0"}

@router.post("/", response_model=GameResponse)
def create_game(
    request: CreateGameRequest, 
    game_service: GameService = Depends(get_game_service),
    creation_service: GameCreationService = Depends(get_game_creation_service)
):
    """
    Cria um novo jogo
    
    Controller Pattern: coordena criação do jogo e seus componentes
    """
    # Cria jogo usando o service
    jogo = creation_service.create_game(request)
    
    # Armazena o jogo
    game_service.save_game(jogo.id, jogo)
    
    # Retorna resposta usando ResponseAssembler
    return ResponseAssembler.montar_criacao_jogo(jogo, incluir_jogadores_detalhados=False)

@router.get("/{game_id}", response_model=GameStateResponse)
def get_game_state(
    ctx: GameRequestContext = Depends(get_game_context),
    longest_path_service: LongestPathService = Depends(get_longest_path_service)
):
    """
    Retorna o estado atual do jogo
    
    Information Expert: Jogo conhece seu próprio estado
    Refatoração DRY: Usa GameRequestContext para eliminar boilerplate
    """
    # Monta estado completo usando ResponseAssembler
    estado = ResponseAssembler.montar_estado_jogo_completo(ctx.jogo)
    
    # Converte jogadores para JogadorResponse (schema do pydantic)
    jogadores = [
        JogadorResponse(
            id=j["id"],
            nome=j["nome"],
            cor=j["cor"],
            trens_disponiveis=j["trens_restantes"],
            pontos=j["pontos"]
        )
        for j in estado["jogadores"]
    ]
    
    # Converte cartas visíveis para CartaVagaoResponse
    cartas_visiveis = [
        CartaVagaoResponse(**carta)
        for carta in estado["cartas_visiveis"]
    ]
    
    maior_caminho_status = longest_path_service.calcular_status(ctx.jogo)

    return GameStateResponse(
        game_id=estado["game_id"],
        iniciado=estado["iniciado"],
        finalizado=estado["finalizado"],
        jogadores=jogadores,
        jogador_atual_id=estado["jogador_atual_id"],
        cartas_visiveis=cartas_visiveis,
        cartas_fechadas_restantes=estado.get("cartas_fechadas_restantes"),
        cartas_fechadas_disponiveis=estado.get("cartas_fechadas_disponiveis"),
        pode_comprar_carta_fechada=estado.get("pode_comprar_carta_fechada"),
        maior_caminho=maior_caminho_status
    )

@router.post("/{game_id}/next-turn")
@auto_save_game
def next_turn(
    ctx: GameRequestContext = Depends(get_game_context),
    action_service: GameActionService = Depends(get_game_action_service)
):
    """
    Passa para o próximo turno
    
    Refatoração DRY:
    - @auto_save_game elimina necessidade de game_service.save_game()
    - GameRequestContext elimina boilerplate de parâmetros
    """
    from ....shared.response_builder import ResponseBuilder
    
    # Avança turno e verifica fim
    resultado_turno = action_service.passar_turno_e_verificar_fim(ctx.jogo)

    return ResponseBuilder.success_with_turn(
        message=f"Turno passado para jogador {resultado_turno['proximo_jogador']}",
        resultado_turno=resultado_turno
    )

@router.get("/{game_id}/pontuacao-final")
def get_pontuacao_final(
    ctx: GameRequestContext = Depends(get_game_context),
    pontuacao_service: PontuacaoFinalService = Depends(get_pontuacao_final_service)
):
    """
    CORREÇÃO BUG #3: Endpoint para calcular e retornar pontuação final
    
    Calcula pontuação final de todos os jogadores e determina vencedor(es).
    Deve ser chamado quando jogo.finalizado == True.
    
    Refatoração DRY: Usa GameRequestContext para eliminar boilerplate
    
    Returns:
        - pontuacoes: Array com pontuação detalhada de cada jogador
        - vencedor: ID do vencedor ou lista de IDs se empate
        - mensagem: Mensagem de resultado
    """
    return pontuacao_service.calcular_resultado_final(ctx.jogo)
