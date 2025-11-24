"""
Ticket Schemas - Schemas relacionados aos bilhetes de destino

Contém requests e responses para compra e gerenciamento de bilhetes.
"""

from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import List


class BilheteDestinoResponse(BaseModel):
    """Response com informações de um bilhete destino"""
    id: str
    cidadeOrigem: str
    cidadeDestino: str
    pontos: int


class BilhetesPendentesResponse(BaseModel):
    """Response com os bilhetes iniciais disponíveis para escolha"""
    player_id: str
    quantidade_disponivel: int
    minimo_escolha: int
    maximo_escolha: int
    bilhetes: List[BilheteDestinoResponse]


class EscolherBilhetesIniciaisRequest(BaseModel):
    """Request para confirmar os bilhetes iniciais escolhidos pelo jogador"""
    bilhetes_escolhidos: List[str] = Field(min_length=2, max_length=4)

    @model_validator(mode="before")
    def normalizar_ids(cls, values):
        bilhetes = values.get("bilhetes_escolhidos", [])
        values["bilhetes_escolhidos"] = [str(b).strip() for b in bilhetes]
        return values

    @model_validator(mode="after")
    def validar_unicidade(self):
        identificadores = self.bilhetes_escolhidos
        if len(set(identificadores)) != len(identificadores):
            raise ValueError("IDs de bilhetes duplicados não são permitidos")
        return self


class EscolhaBilhetesIniciaisResponse(BaseModel):
    """Response após a confirmação dos bilhetes iniciais"""
    success: bool
    player_id: str
    tickets_kept: int
    tickets_returned: int
    bilhetes: List[BilheteDestinoResponse]


class ComprarBilhetesRequest(BaseModel):
    """Request para comprar bilhetes de destino durante o jogo"""
    bilhetes_escolhidos: List[str] = Field(description="IDs dos bilhetes que o jogador escolheu manter")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "bilhetes_escolhidos": ["0", "2"]  # Mantém bilhetes nos índices 0 e 2
            }
        }
    )


class ComprarBilhetesResponse(BaseModel):
    """Response após comprar bilhetes durante o jogo"""
    success: bool
    player_id: str
    bilhetes_mantidos: int
    bilhetes_devolvidos: int
    message: str = ""
