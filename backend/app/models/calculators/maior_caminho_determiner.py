"""
Determinação de jogadores com maior caminho contínuo.

PADRÃO GRASP: Pure Fabrication
- Classe auxiliar para determinar jogadores com maior caminho
- Encapsula lógica de comparação de caminhos entre jogadores
"""

from typing import Dict, List
from .longest_path import LongestPathCalculator
from ..entities.rota import Rota


class MaiorCaminhoDeterminer:
    """
    Pure Fabrication - Determina jogadores com maior caminho contínuo.

    Responsabilidades:
    - Calcular comprimento do maior caminho para cada jogador
    - Identificar jogadores com maior caminho (pode haver empates)
    - Retornar lista de jogadores empatados

    GRASP Principles:
    - Pure Fabrication: Classe criada para responsabilidade específica
    - Information Expert: Conhece algoritmo de determinação
    - Low Coupling: Não depende de outros serviços
    - High Cohesion: Focado apenas em determinação de maior caminho
    """

    def __init__(self, longest_path_calculator: LongestPathCalculator = None):
        """
        Inicializa o determinador.

        Args:
            longest_path_calculator: Calculator para maior caminho (opcional)
        """
        self.longest_path_calculator = longest_path_calculator or LongestPathCalculator()

    def determinar_jogadores_maior_caminho(
        self,
        jogadores_rotas: Dict[str, List[Rota]]
    ) -> List[str]:
        """
        Determina quais jogadores têm o maior caminho contínuo.

        Args:
            jogadores_rotas: {jogador_id: rotas_conquistadas}

        Returns:
            Lista de IDs de jogadores com maior caminho (pode haver múltiplos em caso de empate)

        Exemplo:
            >>> determinador = MaiorCaminhoDeterminer()
            >>> rotas = {
            ...     'alice': [rota1, rota2, rota3],
            ...     'bob': [rota4, rota5]
            ... }
            >>> vencedores = determinador.determinar_jogadores_maior_caminho(rotas)
            >>> print(vencedores)
            ['alice']
        """
        if not jogadores_rotas:
            return []

        # Calcular comprimento para cada jogador
        comprimentos: Dict[str, int] = {}

        for jogador_id, rotas in jogadores_rotas.items():
            comprimento = self.longest_path_calculator.calcular_maior_caminho(rotas)
            comprimentos[jogador_id] = comprimento

        # Encontrar maior comprimento
        if not comprimentos:
            return []

        maior_comprimento = max(comprimentos.values())

        # Retornar todos os jogadores com maior comprimento
        jogadores_com_maior = [
            jogador_id
            for jogador_id, comprimento in comprimentos.items()
            if comprimento == maior_comprimento
        ]

        return jogadores_com_maior

    def calcular_comprimentos_caminhos(
        self,
        jogadores_rotas: Dict[str, List[Rota]]
    ) -> Dict[str, int]:
        """
        Calcula o comprimento do maior caminho para cada jogador.

        Args:
            jogadores_rotas: {jogador_id: rotas_conquistadas}

        Returns:
            {jogador_id: comprimento_maior_caminho}

        Útil para debugging ou quando precisamos dos comprimentos individuais.
        """
        comprimentos: Dict[str, int] = {}

        for jogador_id, rotas in jogadores_rotas.items():
            comprimento = self.longest_path_calculator.calcular_maior_caminho(rotas)
            comprimentos[jogador_id] = comprimento

        return comprimentos