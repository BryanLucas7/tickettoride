"""
Factories para Application Services.

Padrão GRASP: Pure Fabrication
Padrão GoF: Factory Method
Arquitetura: Application Layer (Use Cases)

Este módulo fornece factories para criar instâncias de services.
Services são injetados via FastAPI Depends().
"""

from fastapi import Depends

from ..core.ports.repositories.jogo_repository_port import JogoRepositoryPort
from ..application.services.game_service import GameService
from ..application.services.game_action_service import GameActionService
from ..application.services.game_creation_service import GameCreationService
from ..application.services.pontuacao_final_service import PontuacaoFinalService
from ..application.services.route_conquest_service import RouteConquestService
from ..application.services.ticket_purchase_service import TicketPurchaseService
from ..application.services.longest_path_service import LongestPathService

from .repositories import get_jogo_repository

# Instância única para reaproveitar cache de jogos e evitar _sync e loads repetidos
_GAME_SERVICE_SINGLETON: GameService | None = None


def get_game_service(
    repository: JogoRepositoryPort = Depends(get_jogo_repository)
) -> GameService:
    """
    Dependency para injetar GameService com Repository Pattern.
    GameService agora usa o repository injetado.
    """
    global _GAME_SERVICE_SINGLETON

    if _GAME_SERVICE_SINGLETON is None:
        _GAME_SERVICE_SINGLETON = GameService(repository=repository)

    return _GAME_SERVICE_SINGLETON


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
