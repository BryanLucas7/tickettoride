"""
Dependências FastAPI para injeção de services com Repository Pattern.
Adapters para Arquitetura Hexagonal.
"""
from fastapi import Depends, HTTPException

# Core Ports
from .core.ports.repositories.jogo_repository_port import JogoRepositoryPort

# Outbound Adapters (Implementations)
from .adapters.outbound.persistence.pickle_jogo_repository import PickleJogoRepository

# Core Domain
from .core.domain.entities.jogo import Jogo
from .core.domain.entities.jogador import Jogador

# Infrastructure Services (Application Layer)
from .application.services.game_service import GameService
from .application.services.game_action_service import GameActionService
from .application.services.game_creation_service import GameCreationService
from .application.services.pontuacao_final_service import PontuacaoFinalService
from .application.services.route_conquest_service import RouteConquestService
from .application.services.ticket_purchase_service import TicketPurchaseService
from .application.services.longest_path_service import LongestPathService


# ============================================================================
# OUTBOUND ADAPTERS (Secondary - Persistence)
# ============================================================================

def get_jogo_repository() -> JogoRepositoryPort:
    """
    Factory para JogoRepository.
    Retorna implementação com Pickle (pode ser trocada por DB posteriormente).
    """
    return PickleJogoRepository()


# ============================================================================
# INFRASTRUCTURE SERVICES (Application Layer)
# ============================================================================

def get_game_service(
    repository: JogoRepositoryPort = Depends(get_jogo_repository)
) -> GameService:
    """
    Dependency para injetar GameService com Repository Pattern.
    GameService agora usa o repository injetado.
    """
    return GameService(repository=repository)


def get_game_action_service() -> GameActionService:
    """Dependency para injetar GameActionService."""
    return GameActionService()


def get_game_creation_service() -> GameCreationService:
    """Dependency para injetar GameCreationService."""
    return GameCreationService()


def get_pontuacao_final_service() -> PontuacaoFinalService:
    """Dependency para injetar PontuacaoFinalService."""
    return PontuacaoFinalService()


def get_route_conquest_service() -> RouteConquestService:
    """Dependency para injetar RouteConquestService."""
    return RouteConquestService()


def get_ticket_purchase_service(
    action_service: GameActionService = Depends(get_game_action_service)
) -> TicketPurchaseService:
    """Dependency para injetar TicketPurchaseService."""
    return TicketPurchaseService(action_service=action_service)


def get_longest_path_service() -> LongestPathService:
    """Dependency para injetar LongestPathService."""
    return LongestPathService()


# ============================================================================
# VALIDATION HELPERS - FastAPI Dependency Injection
# ============================================================================
# 
# Estas dependências substituem os decorators/helpers antigos (REMOVIDOS):
# - decorators/validation.py (@require_game, @require_game_and_player)  
# - utils/validation_helpers.py (validate_game, validate_game_and_player)
# - GameValidators.validar_jogo_existe() e validar_jogo_e_jogador()
#
# Uso idiomático com FastAPI Depends():
#
#   @router.get("/games/{game_id}/...")
#   def endpoint(
#       game_id: str,
#       jogo: Jogo = Depends(get_validated_game)
#   ):
#       # jogo já está validado e pronto para uso
#       ...
#
#   @router.get("/games/{game_id}/players/{player_id}/...")
#   def endpoint(
#       game_id: str,
#       player_id: str,
#       jogador: Jogador = Depends(get_validated_player),
#       jogo: Jogo = Depends(get_validated_game)  # opcional se também precisar do jogo
#   ):
#       # jogador e jogo validados
#       ...
# ============================================================================

def get_validated_game(
    game_id: str,
    game_service: GameService = Depends(get_game_service)
) -> Jogo:
    """
    Valida e retorna o jogo.
    
    GRASP Controller: Coordena validação de jogo via GameService.
    Substitui padrão duplicado em múltiplos lugares do código.
    
    Args:
        game_id: ID do jogo
        game_service: Service injetado automaticamente
        
    Returns:
        Jogo validado
        
    Raises:
        HTTPException(404): Se jogo não existir
        
    Usage:
        @router.get("/games/{game_id}/state")
        def get_state(
            game_id: str,
            jogo: Jogo = Depends(get_validated_game)
        ):
            return {"state": jogo.iniciado}
    """
    jogo = game_service.get_game(game_id)
    if not jogo:
        raise HTTPException(status_code=404, detail=f"Game {game_id} not found")
    return jogo


def get_validated_player(
    game_id: str,
    player_id: str,
    jogo: Jogo = Depends(get_validated_game)
) -> Jogador:
    """
    Valida e retorna o jogador. Já inclui validação do jogo.
    
    GRASP Controller: Coordena validação de jogador.
    Information Expert: Usa GerenciadorDeTurnos.obter_jogador_por_id().
    
    Args:
        game_id: ID do jogo
        player_id: ID do jogador
        jogo: Jogo já validado (injetado automaticamente)
        
    Returns:
        Jogador validado
        
    Raises:
        HTTPException(404): Se jogador não existir
        
    Usage:
        @router.get("/games/{game_id}/players/{player_id}/cards")
        def get_cards(
            game_id: str,
            player_id: str,
            jogador: Jogador = Depends(get_validated_player)
        ):
            return {"cards": jogador.mao.cartasVagao}
    """
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"🔍 DEBUG get_validated_player - game_id: {game_id}, player_id: {player_id}")
    
    jogador = jogo.gerenciadorDeTurnos.obter_jogador_por_id(player_id)
    if not jogador:
        logger.error(f"❌ Jogador {player_id} não encontrado no jogo!")
        raise HTTPException(status_code=404, detail=f"Player {player_id} not found")
    
    logger.info(f"✅ Jogador {player_id} encontrado")
    return jogador