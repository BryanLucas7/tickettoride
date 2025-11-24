"""
Route Schemas - Schemas relacionados às rotas do tabuleiro

Contém requests e responses para conquista e consulta de rotas.
"""

from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class ConquistarRotaRequest(BaseModel):
    """Request para conquistar uma rota"""
    rota_id: str
    cartas_usadas: List[str]  # Lista de cores como strings
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "rota_id": "sao_paulo_rio",
                "cartas_usadas": ["vermelho", "vermelho", "vermelho"]
            }
        }
    )


class ConquistarRotaResponse(BaseModel):
    """Response após conquistar uma rota"""
    success: bool
    player_id: str
    rota_id: str
    pontos_ganhos: int
    trens_restantes: int
    message: str = ""


class RotaResponse(BaseModel):
    """Response com informações de uma rota"""
    id: str
    cidadeOrigem: str
    cidadeDestino: str
    comprimento: int
    cor: Optional[str]
    conquistada: bool
    jogador_dono: Optional[str] = None


class RotaDisponibilidadeResponse(BaseModel):
    """Response com disponibilidade de rotas"""
    rotas_disponiveis: List[RotaResponse]
    total: int
