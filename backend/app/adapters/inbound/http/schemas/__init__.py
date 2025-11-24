"""
Schemas para a API HTTP (Inbound Adapter)

Organização modular dos schemas Pydantic por domínio.
"""

# Common schemas
from .common_schemas import (
    CorEnum,
    CartaVagaoResponse,
    ErrorResponse,
    SuccessResponse,
)

# Game schemas
from .game_schemas import (
    CreateGameRequest,
    GameResponse,
    GameStateResponse,
    MaiorCaminhoLeaderResponse,
    MaiorCaminhoStatusResponse,
)

# Player schemas
from .player_schemas import (
    JogadorSetup,
    JogadorResponse,
    MaoResponse,
    ComprarCartaRequest,
    ComprarCartaResponse,
)

# Ticket schemas
from .ticket_schemas import (
    BilheteDestinoResponse,
    BilhetesPendentesResponse,
    EscolherBilhetesIniciaisRequest,
    EscolhaBilhetesIniciaisResponse,
    ComprarBilhetesRequest,
    ComprarBilhetesResponse,
)

# Route schemas
from .route_schemas import (
    ConquistarRotaRequest,
    ConquistarRotaResponse,
    RotaResponse,
    RotaDisponibilidadeResponse,
)

__all__ = [
    # Common
    "CorEnum",
    "CartaVagaoResponse",
    "ErrorResponse",
    "SuccessResponse",
    
    # Game
    "CreateGameRequest",
    "GameResponse",
    "GameStateResponse",
    "MaiorCaminhoLeaderResponse",
    "MaiorCaminhoStatusResponse",
    
    # Player
    "JogadorSetup",
    "JogadorResponse",
    "MaoResponse",
    "ComprarCartaRequest",
    "ComprarCartaResponse",
    
    # Ticket
    "BilheteDestinoResponse",
    "BilhetesPendentesResponse",
    "EscolherBilhetesIniciaisRequest",
    "EscolhaBilhetesIniciaisResponse",
    "ComprarBilhetesRequest",
    "ComprarBilhetesResponse",
    
    # Route
    "ConquistarRotaRequest",
    "ConquistarRotaResponse",
    "RotaResponse",
    "RotaDisponibilidadeResponse",
]
