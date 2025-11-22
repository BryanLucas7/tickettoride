"""
TASK #82: API - Endpoints completos de ações de jogo

Define tipos e estruturas de dados para ações de turno.

GoF Patterns: N/A (apenas tipos)

GRASP Principles:
- Information Expert: Tipos conhecem sua estrutura de dados
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
from enum import Enum


class TipoAcao(Enum):
    """Tipos de ações possíveis no turno"""
    COMPRAR_CARTAS = "comprar_cartas"
    CONQUISTAR_ROTA = "conquistar_rota"
    COMPRAR_BILHETES = "comprar_bilhetes"
    PASSAR_TURNO = "passar_turno"


@dataclass
class ResultadoAcao:
    """Resultado da execução de uma ação"""
    sucesso: bool
    mensagem: str
    dados: Dict[str, Any] = field(default_factory=dict)
    erros: List[str] = field(default_factory=list)