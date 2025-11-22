"""
Dependências FastAPI para injeção de services stateful via app.state.
"""
from fastapi import Depends, Request

from .services.game_service import GameService


def get_game_service(request: Request) -> GameService:
    """Dependency para injetar GameService singleton."""
    if not hasattr(request.app.state, "game_service"):
        raise RuntimeError("GameService não inicializado. Verifique lifespan.")
    return request.app.state.game_service