"""
Common Schemas - Schemas compartilhados entre diferentes módulos

Contém enums e schemas básicos usados em toda a API.
"""

from pydantic import BaseModel, Field
from enum import Enum


class CorEnum(str, Enum):
    """Enum para as cores das cartas de vagão"""
    VERMELHO = "vermelho"
    LARANJA = "laranja"
    AMARELO = "amarelo"
    VERDE = "verde"
    AZUL = "azul"
    PRETO = "preto"
    BRANCO = "branco"
    ROXO = "roxo"
    LOCOMOTIVA = "locomotiva"


class CartaVagaoResponse(BaseModel):
    """Response com informações de uma carta de vagão"""
    cor: CorEnum
    eh_locomotiva: bool = Field(description="Indica se a carta é locomotiva")


class ErrorResponse(BaseModel):
    """Response padrão para erros"""
    error: str
    detail: str = ""


class SuccessResponse(BaseModel):
    """Response padrão para operações bem-sucedidas"""
    success: bool
    message: str = ""
