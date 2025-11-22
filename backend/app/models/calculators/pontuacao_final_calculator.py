"""
Cálculo de pontuação final de jogadores.

PADRÃO GRASP: Information Expert
- PontuacaoFinalCalculator conhece regras de pontuação
- Calcula pontuação completa de um jogador
"""

from dataclasses import dataclass, field
from typing import List, Dict
from .verificador_bilhetes import VerificadorBilhetes
from .longest_path import LongestPathCalculator
from .pontuacao_final_types import ResultadoJogador
from ..entities.rota import Rota
from ..entities.bilhete_destino import BilheteDestino


@dataclass
class PontuacaoFinalCalculator:
    """
    Information Expert - Calcula pontuação final completa.

    Responsabilidades:
    - Calcular pontuação de cada jogador
    - Aplicar bônus de maior caminho
    - Determinar vencedor com critérios de desempate

    GRASP Principles:
    - Information Expert: Conhece regras de pontuação
    - Low Coupling: Usa componentes especializados
    - High Cohesion: Focado em pontuação final
    """

    verificador_bilhetes: VerificadorBilhetes = field(default_factory=VerificadorBilhetes)
    longest_path_calculator: LongestPathCalculator = field(default_factory=LongestPathCalculator)

    def calcular_pontuacao_jogador(
        self,
        jogador_id: str,
        pontos_rotas: int,
        bilhetes: List[BilheteDestino],
        rotas_conquistadas: List[Rota],
        tem_maior_caminho: bool = False
    ) -> ResultadoJogador:
        """
        Calcula pontuação final de um jogador.

        Args:
            jogador_id: ID do jogador
            pontos_rotas: Pontos já acumulados de rotas durante o jogo
            bilhetes: Lista de bilhetes do jogador
            rotas_conquistadas: Lista de rotas conquistadas pelo jogador
            tem_maior_caminho: Se jogador tem maior caminho (+10 pts)

        Returns:
            ResultadoJogador com pontuação detalhada
        """
        # Calcular bilhetes completos e incompletos
        bilhetes_completos = self.verificador_bilhetes.listar_bilhetes_completos(
            bilhetes=bilhetes,
            rotas_conquistadas=rotas_conquistadas
        )

        bilhetes_incompletos = self.verificador_bilhetes.listar_bilhetes_incompletos(
            bilhetes=bilhetes,
            rotas_conquistadas=rotas_conquistadas
        )

        # Calcular pontos de bilhetes
        pontos_completos = sum(b.pontos for b in bilhetes_completos)
        pontos_incompletos = -sum(b.pontos for b in bilhetes_incompletos)  # negativo

        # Calcular maior caminho
        comprimento_caminho = self.longest_path_calculator.calcular_maior_caminho(rotas_conquistadas)

        # Bônus de maior caminho
        bonus = 10 if tem_maior_caminho else 0

        return ResultadoJogador(
            jogador_id=jogador_id,
            pontos_rotas=pontos_rotas,
            pontos_bilhetes_completos=pontos_completos,
            pontos_bilhetes_incompletos=pontos_incompletos,
            bonus_maior_caminho=bonus,
            bilhetes_completos=len(bilhetes_completos),
            bilhetes_incompletos=len(bilhetes_incompletos),
            comprimento_maior_caminho=comprimento_caminho,
            bilhetes_completos_lista=bilhetes_completos,
            bilhetes_incompletos_lista=bilhetes_incompletos
        )

    def determinar_vencedor(
        self,
        resultados: Dict[str, ResultadoJogador]
    ) -> str | List[str]:
        """
        Determina vencedor com critérios de desempate.

        Critérios (em ordem):
        1. Maior pontuação total
        2. Mais bilhetes completos
        3. Maior caminho contínuo (comprimento)
        4. Empate permanece

        Args:
            resultados: Dicionário {jogador_id: ResultadoJogador}

        Returns:
            ID do vencedor ou lista de IDs se empate
        """
        if not resultados:
            return []

        # Ordenar por critérios
        jogadores_ordenados = sorted(
            resultados.items(),
            key=lambda x: (
                x[1].pontuacao_total,
                x[1].bilhetes_completos,
                x[1].comprimento_maior_caminho
            ),
            reverse=True
        )

        # Pegar primeiro (maior pontuação)
        vencedor_id, vencedor_resultado = jogadores_ordenados[0]

        # Verificar empates
        empatados = [vencedor_id]

        for jogador_id, resultado in jogadores_ordenados[1:]:
            # Empate total (mesmos critérios)
            if (
                resultado.pontuacao_total == vencedor_resultado.pontuacao_total and
                resultado.bilhetes_completos == vencedor_resultado.bilhetes_completos and
                resultado.comprimento_maior_caminho == vencedor_resultado.comprimento_maior_caminho
            ):
                empatados.append(jogador_id)
            else:
                break  # Não empata mais

        # Retornar único ou lista
        if len(empatados) == 1:
            return empatados[0]
        else:
            return empatados