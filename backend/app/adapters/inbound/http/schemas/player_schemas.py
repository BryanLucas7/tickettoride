"""
Player Schemas - Schemas relacionados aos jogadores

Contém requests e responses para ações e informações de jogadores.
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List


class JogadorSetup(BaseModel):
    """Dados enviados pelo frontend para configurar um jogador"""
    nome: str = Field(min_length=1, max_length=100)
    cor: str = Field(min_length=1, description="Nome da cor correspondente ao enum Cor")

    @field_validator("nome")
    def validar_nome(cls, value: str) -> str:
        nome = value.strip()
        if not nome:
            raise ValueError("Nome do jogador não pode ser vazio")
        return nome

    @field_validator("cor")
    def normalizar_cor(cls, value: str) -> str:
        return value.strip()


class JogadorResponse(BaseModel):
    """Response com informações do jogador"""
    id: str  # UUID string
    nome: str
    cor: str
    trens_disponiveis: int
    pontos: int


class MaoResponse(BaseModel):
    """Response com informações da mão de um jogador"""
    player_id: str
    cartas_vagao: dict = Field(description="Dicionário com contagem de cartas por cor")
    total_cartas: int


class ComprarCartaRequest(BaseModel):
    """Request para comprar cartas"""
    player_id: str  # UUID string
    card_indices: List[int] = Field(description="Índices das cartas visíveis a comprar (0-4), ou lista vazia para comprar do monte")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "player_id": "0",
                "card_indices": [0, 2]  # Compra 1ª e 3ª carta visível
            }
        }
    )


class ComprarCartaResponse(BaseModel):
    """Response após comprar cartas"""
    success: bool
    player_id: str
    cartas_compradas: int
    pode_comprar_mais: bool
    message: str = ""
