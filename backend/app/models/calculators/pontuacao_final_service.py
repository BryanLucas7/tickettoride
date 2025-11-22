"""
Coordenação de cálculo de pontuação final.

PADRÃO GRASP: Controller
- PontuacaoFinalService coordena cálculo de pontuação final
- Orquestra componentes: bilhetes, rotas, maior caminho
- Determina vencedor e aplica critérios de desempate
"""

from dataclasses import dataclass, field
from typing import Dict, List
from .pontuacao_final_calculator import PontuacaoFinalCalculator
from .pontuacao_final_types import ResultadoFinal, ResultadoJogador
from .maior_caminho_determiner import MaiorCaminhoDeterminer
from ..entities.rota import Rota


@dataclass
class PontuacaoFinalService:
    """
    Controller - Coordena cálculo de pontuação final.

    Responsabilidades:
    - Orquestrar cálculo de pontuação de todos os jogadores
    - Determinar jogadores com maior caminho
    - Aplicar bônus de maior caminho
    - Determinar vencedor final
    - Gerar ranking

    GRASP Principles:
    - Controller: Coordena fluxo de pontuação final
    - Low Coupling: Delega cálculos especializados
    - High Cohesion: Focado em coordenação de pontuação
    """

    calculator: PontuacaoFinalCalculator = field(default_factory=PontuacaoFinalCalculator)
    maior_caminho_determiner: MaiorCaminhoDeterminer = field(default_factory=MaiorCaminhoDeterminer)

    def calcular_resultado_final(
        self,
        jogadores_dados: Dict[str, Dict]
    ) -> ResultadoFinal:
        """
        Calcula resultado final do jogo.

        Args:
            jogadores_dados: Dicionário {
                jogador_id: {
                    'pontos_rotas': int,
                    'bilhetes': List[BilheteDestino],
                    'rotas_conquistadas': List[Rota]
                }
            }

        Returns:
            ResultadoFinal com todos os resultados

        Exemplo:
            >>> service = PontuacaoFinalService()
            >>> dados = {
            ...     'alice': {
            ...         'pontos_rotas': 30,
            ...         'bilhetes': [bilhete1, bilhete2],
            ...         'rotas_conquistadas': [rota1, rota2, rota3]
            ...     },
            ...     'bob': {
            ...         'pontos_rotas': 25,
            ...         'bilhetes': [bilhete3],
            ...         'rotas_conquistadas': [rota4, rota5]
            ...     }
            ... }
            >>> resultado = service.calcular_resultado_final(dados)
            >>> print(resultado.vencedor)
            'alice'
        """
        # 1. Determinar jogadores com maior caminho
        jogadores_rotas = {
            jogador_id: dados['rotas_conquistadas']
            for jogador_id, dados in jogadores_dados.items()
        }

        jogadores_com_maior = self.maior_caminho_determiner.determinar_jogadores_maior_caminho(jogadores_rotas)

        # 2. Calcular pontuação de cada jogador
        resultados: Dict[str, ResultadoJogador] = {}

        for jogador_id, dados in jogadores_dados.items():
            tem_maior = jogador_id in jogadores_com_maior

            resultado = self.calculator.calcular_pontuacao_jogador(
                jogador_id=jogador_id,
                pontos_rotas=dados['pontos_rotas'],
                bilhetes=dados['bilhetes'],
                rotas_conquistadas=dados['rotas_conquistadas'],
                tem_maior_caminho=tem_maior
            )

            resultados[jogador_id] = resultado

        # 3. Determinar vencedor
        vencedor = self.calculator.determinar_vencedor(resultados)

        # 4. Gerar ranking
        ranking = self._gerar_ranking(resultados)

        return ResultadoFinal(
            resultados=resultados,
            vencedor=vencedor,
            jogadores_com_maior_caminho=jogadores_com_maior,
            ranking=ranking
        )

    def _gerar_ranking(
        self,
        resultados: Dict[str, ResultadoJogador]
    ) -> List[str]:
        """
        Gera ranking de jogadores ordenado por pontuação.

        Args:
            resultados: {jogador_id: ResultadoJogador}

        Returns:
            Lista de jogador_ids ordenados (primeiro = vencedor)
        """
        jogadores_ordenados = sorted(
            resultados.items(),
            key=lambda x: (
                x[1].pontuacao_total,
                x[1].bilhetes_completos,
                x[1].comprimento_maior_caminho
            ),
            reverse=True
        )

        return [jogador_id for jogador_id, _ in jogadores_ordenados]