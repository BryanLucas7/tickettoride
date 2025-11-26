"""
Dependências FastAPI para injeção de services com Repository Pattern.
Adapters para Arquitetura Hexagonal.

Módulo organizado em três responsabilidades (SRP):
- repositories: Factories para persistence adapters
- services: Factories para application services  
- validators: Dependências de validação (game, player)

Uso:
    from app.dependencies import (
        # Repositories
        get_jogo_repository,
        
        # Services
        get_game_service,
        get_game_action_service,
        get_game_creation_service,
        get_pontuacao_final_service,
        get_route_conquest_service,
        get_ticket_purchase_service,
        get_longest_path_service,
        
        # Validators
        get_validated_game,
        get_validated_player
    )
"""

# Re-export tudo para manter compatibilidade retroativa
from .repositories import get_jogo_repository
from .services import (
    get_game_service,
    get_game_action_service,
    get_game_creation_service,
    get_pontuacao_final_service,
    get_route_conquest_service,
    get_ticket_purchase_service,
    get_longest_path_service,
)
from .validators import (
    get_validated_game,
    get_validated_player,
)

__all__ = [
    # Repositories
    "get_jogo_repository",
    # Services
    "get_game_service",
    "get_game_action_service",
    "get_game_creation_service",
    "get_pontuacao_final_service",
    "get_route_conquest_service",
    "get_ticket_purchase_service",
    "get_longest_path_service",
    # Validators
    "get_validated_game",
    "get_validated_player",
]
