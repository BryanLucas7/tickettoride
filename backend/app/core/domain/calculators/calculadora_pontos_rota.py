"""
Calculadora de pontos para rotas conquistadas.

PADRÃO GRASP: Pure Fabrication
- Classe auxiliar para cálculo de pontos de rotas
- Encapsula tabela de pontuação
"""

from typing import Dict
from app.constants import TABELA_PONTOS_ROTA


class CalculadoraPontosRota:
    """
    Pure Fabrication - Calcula pontos de rotas conquistadas.

    Responsabilidades:
    - Conhecer tabela de pontuação por comprimento
    - Calcular pontos baseado no comprimento da rota

    GRASP Principles:
    - Pure Fabrication: Classe criada para responsabilidade específica
    - Information Expert: Conhece regras de pontuação
    - Low Coupling: Não depende de outras classes
    - High Cohesion: Focado apenas em cálculo de pontos
    """

    # Tabela de pontuação importada de constantes centralizadas
    _TABELA_PONTOS: Dict[int, int] = TABELA_PONTOS_ROTA

    @classmethod
    def calcular_pontos(cls, comprimento: int) -> int:
        """
        Calcula pontos para uma rota de determinado comprimento.

        Args:
            comprimento: Comprimento da rota em vagões

        Returns:
            Pontos ganhos pela conquista

        Exemplo:
            >>> CalculadoraPontosRota.calcular_pontos(3)
            4
            >>> CalculadoraPontosRota.calcular_pontos(6)
            15
        """
        return cls._TABELA_PONTOS.get(comprimento, 0)

    @classmethod
    def get_tabela_pontos(cls) -> Dict[int, int]:
        """
        Retorna a tabela completa de pontuação.

        Útil para UI ou documentação.
        """
        return cls._TABELA_PONTOS.copy()