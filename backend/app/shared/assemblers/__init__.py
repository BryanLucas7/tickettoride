"""
Assemblers especializados para formatação de respostas da API.

Refatoração SRP: Separação do ResponseAssembler monolítico em assemblers especializados.

Estrutura:
- GameStateAssembler: Estado do jogo e cartas visíveis
- PlayerHandAssembler: Mão do jogador e bilhetes
- ScoreAssembler: Pontuação final e ranking
- RouteAssembler: Painel de rotas do tabuleiro
- GameCreationAssembler: Resposta de criação de jogo
- ConquestResponseAssembler: Resposta de conquista de rotas
- CompraStateAssembler: Estado de compra de cartas
"""

from .game_state_assembler import GameStateAssembler
from .player_hand_assembler import PlayerHandAssembler
from .score_assembler import ScoreAssembler
from .route_assembler import RouteAssembler
from .game_creation_assembler import GameCreationAssembler
from .conquest_response_assembler import ConquestResponseAssembler
from .compra_state_assembler import CompraStateAssembler

__all__ = [
    "GameStateAssembler",
    "PlayerHandAssembler", 
    "ScoreAssembler",
    "RouteAssembler",
    "GameCreationAssembler",
    "ConquestResponseAssembler",
    "CompraStateAssembler"
]
