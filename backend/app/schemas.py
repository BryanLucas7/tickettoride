"""
Schemas Pydantic para a API FastAPI

Este módulo define os modelos de dados para requests/responses da API.
Segue o princípio GRASP de Pure Fabrication - criamos classes específicas
para a camada de API que não pertencem ao domínio do jogo.
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List
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


class CreateGameRequest(BaseModel):
    """Request para criar um novo jogo"""
    numero_jogadores: int = Field(ge=2, le=5, description="Número de jogadores (2-5)")
    jogadores: Optional[List[JogadorSetup]] = Field(
        default=None,
        min_length=2,
        max_length=5,
        description="Lista opcional de jogadores personalizados"
    )
    
    class Config:
        json_schema_extra = {
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
    
    class Config:
        json_schema_extra = {
            "example": {
                "game_id": "game-123",
                "numero_jogadores": 4,
                "iniciado": True,
                "finalizado": False
            }
        }


class JogadorResponse(BaseModel):
    """Response com informações do jogador"""
    id: str  # UUID string
    nome: str
    cor: str
    trens_disponiveis: int
    pontos: int


class CartaVagaoResponse(BaseModel):
    """Response com informações de uma carta de vagão"""
    cor: CorEnum
    eh_locomotiva: bool = Field(description="Indica se a carta é locomotiva")


class BilheteDestinoResponse(BaseModel):
    """Response com informações de um bilhete destino"""
    id: str
    cidadeOrigem: str
    cidadeDestino: str
    pontos: int


class MaiorCaminhoLeaderResponse(BaseModel):
    """Informações do jogador que lidera o maior caminho"""
    jogador_id: str
    jogador_nome: str
    jogador_cor: str


class MaiorCaminhoStatusResponse(BaseModel):
    """Status agregado do maior caminho contínuo durante o jogo"""
    comprimento: int
    lideres: List[MaiorCaminhoLeaderResponse]


class GameStateResponse(BaseModel):
    """Response com estado completo do jogo"""
    game_id: str
    iniciado: bool
    finalizado: bool
    jogadores: List[JogadorResponse]
    jogador_atual_id: Optional[str] = None  # UUID string
    cartas_visiveis: List[CartaVagaoResponse]
    maior_caminho: Optional[MaiorCaminhoStatusResponse] = None
    
    class Config:
        json_schema_extra = {
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


class BuyCardsRequest(BaseModel):
    """Request para comprar cartas"""
    player_id: str  # UUID string
    card_indices: List[int] = Field(description="Índices das cartas visíveis a comprar (0-4), ou lista vazia para comprar do monte")
    
    class Config:
        json_schema_extra = {
            "example": {
                "player_id": "0",
                "card_indices": [0, 2]  # Compra 1ª e 3ª carta visível
            }
        }


class ConquistarRotaRequest(BaseModel):
    """Request para conquistar uma rota"""
    player_id: str  # UUID string
    rota_id: str
    cartas_usadas: List[CorEnum]
    
    class Config:
        json_schema_extra = {
            "example": {
                "player_id": "0",
                "rota_id": "sao_paulo_rio",
                "cartas_usadas": ["vermelho", "vermelho", "vermelho"]
            }
        }


class ComprarBilhetesRequest(BaseModel):
    """Request para comprar bilhetes de destino"""
    bilhetes_escolhidos: List[str] = Field(description="IDs dos bilhetes que o jogador escolheu manter (índices 0-2)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "bilhetes_escolhidos": ["0", "2"]  # Mantém bilhetes nos índices 0 e 2
            }
        }


class BilhetesPendentesResponse(BaseModel):
    """Response com os bilhetes iniciais disponíveis para escolha"""
    player_id: str
    quantidade_disponivel: int
    minimo_escolha: int
    maximo_escolha: int
    bilhetes: List[BilheteDestinoResponse]


class EscolherBilhetesIniciaisRequest(BaseModel):
    """Request para confirmar os bilhetes iniciais escolhidos pelo jogador"""
    bilhetes_escolhidos: List[str] = Field(min_length=2, max_length=3)

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
