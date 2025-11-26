"""
Game Schemas - Schemas relacionados ao gerenciamento de jogos

Contém requests e responses para criação, consulta e estado de jogos.
"""

from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import Optional, List
from .common_schemas import CartaVagaoResponse
from .player_schemas import JogadorSetup, JogadorResponse


class CreateGameRequest(BaseModel):
    """Request para criar um novo jogo"""
    numero_jogadores: int = Field(ge=2, le=5, description="Número de jogadores (2-5)")
    jogadores: Optional[List[JogadorSetup]] = Field(
        default=None,
        min_length=2,
        max_length=5,
        description="Lista opcional de jogadores personalizados"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "numero_jogadores": 4,
                "jogadores": [
                    {"nome": "Alice", "cor": "VERMELHO"},
                    {"nome": "Bob", "cor": "AZUL"},
                    {"nome": "Carol", "cor": "VERDE"},
                    {"nome": "Diana", "cor": "AMARELO"}
                ]
            }
        }
    )

    @model_validator(mode="after")
    def validar_coerencia(self):
        jogadores = self.jogadores or []

        if jogadores:
            total = len(jogadores)
            if total < 2 or total > 5:
                raise ValueError("Lista de jogadores deve conter entre 2 e 5 jogadores")
            self.numero_jogadores = total

        return self


class GameResponse(BaseModel):
    """Response com informações básicas do jogo"""
    game_id: str
    numero_jogadores: int
    iniciado: bool
    finalizado: bool
    jogadores: Optional[List[dict]] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "game_id": "game-123",
                "numero_jogadores": 4,
                "iniciado": True,
                "finalizado": False
            }
        }
    )


class MaiorCaminhoLeaderResponse(BaseModel):
    """Informações do jogador que lidera o maior caminho"""
    jogador_id: str
    jogador_nome: str
    jogador_cor: str


class MaiorCaminhoStatusResponse(BaseModel):
    """Status agregado do maior caminho contínuo durante o jogo"""
    comprimento: int
    lideres: List[MaiorCaminhoLeaderResponse]
    caminho: Optional[List[str]] = None


class GameStateResponse(BaseModel):
    """Response com estado completo do jogo"""
    game_id: str
    iniciado: bool
    finalizado: bool
    jogadores: List[JogadorResponse]
    jogador_atual_id: Optional[str] = None  # UUID string
    cartas_visiveis: List[CartaVagaoResponse]
    cartas_fechadas_restantes: Optional[int] = None
    cartas_fechadas_disponiveis: Optional[int] = None
    pode_comprar_carta_fechada: Optional[bool] = None
    bilhetes_restantes: Optional[int] = None
    maior_caminho: Optional[MaiorCaminhoStatusResponse] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "game_id": "game-123",
                "iniciado": True,
                "finalizado": False,
                "jogadores": [
                    {
                        "id": 0,
                        "nome": "Jogador 1",
                        "cor": "vermelho",
                        "trens_disponiveis": 45,
                        "pontos": 10
                    }
                ],
                "jogador_atual_id": 0,
                "cartas_visiveis": [
                    {"cor": "vermelho", "eh_locomotiva": False},
                    {"cor": "locomotiva", "eh_locomotiva": True}
                ],
                "maior_caminho": {
                    "comprimento": 8,
                    "lideres": [
                        {"jogador_id": "0", "jogador_nome": "Jogador 1", "jogador_cor": "vermelho"}
                    ]
                }
            }
        }
    )
