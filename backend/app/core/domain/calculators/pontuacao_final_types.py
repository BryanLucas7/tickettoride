"""
Tipos de dados para pontuação final.

Contém apenas estruturas de dados (DTOs) para resultados de pontuação.
Não contém lógica de negócio.
"""

from dataclasses import dataclass, field
from typing import List, Dict
from app.core.domain.entities.bilhete_destino import BilheteDestino


@dataclass
class ResultadoJogador:
    """
    Resultado final de um jogador.

    Atributos:
        jogador_id: ID do jogador
        pontos_rotas: Pontos de rotas conquistadas
        pontos_bilhetes_completos: Pontos de bilhetes completos
        pontos_bilhetes_incompletos: Pontos perdidos de bilhetes incompletos (negativo)
        bonus_maior_caminho: +10 se tem maior caminho, 0 caso contrário
        pontuacao_total: Soma de todos os pontos
        bilhetes_completos: Quantidade de bilhetes completos
        bilhetes_incompletos: Quantidade de bilhetes incompletos
        comprimento_maior_caminho: Comprimento do maior caminho contínuo
        bilhetes_completos_lista: Referência aos objetos de bilhetes completos
        bilhetes_incompletos_lista: Referência aos objetos de bilhetes incompletos
    """
    jogador_id: str
    pontos_rotas: int = 0
    pontos_bilhetes_completos: int = 0
    pontos_bilhetes_incompletos: int = 0
    bonus_maior_caminho: int = 0
    pontuacao_total: int = 0
    bilhetes_completos: int = 0
    bilhetes_incompletos: int = 0
    comprimento_maior_caminho: int = 0
    bilhetes_completos_lista: List[BilheteDestino] = field(default_factory=list)
    bilhetes_incompletos_lista: List[BilheteDestino] = field(default_factory=list)

    def __post_init__(self):
        """Calcula pontuação total automaticamente"""
        self.pontuacao_total = (
            self.pontos_rotas +
            self.pontos_bilhetes_completos +
            self.pontos_bilhetes_incompletos +  # já é negativo
            self.bonus_maior_caminho
        )


@dataclass
class ResultadoFinal:
    """
    Resultado final do jogo.

    Atributos:
        resultados: Dicionário {jogador_id: ResultadoJogador}
        vencedor: ID do jogador vencedor (ou lista se empate)
        jogadores_com_maior_caminho: Lista de IDs com maior caminho (+10 pts)
        ranking: Lista de jogador_ids ordenados por pontuação
    """
    resultados: Dict[str, ResultadoJogador]
    vencedor: str | List[str]
    jogadores_com_maior_caminho: List[str]
    ranking: List[str]