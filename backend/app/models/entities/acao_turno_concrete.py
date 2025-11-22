"""
TASK #82: API - Endpoints completos de ações de jogo

Implementa ações concretas de turno usando Template Method Pattern.

GoF Patterns:
1. Template Method Pattern - Ações concretas implementam template

GRASP Principles:
- Information Expert: Cada ação conhece suas regras específicas
"""

from typing import List

from .acao_turno_base import AcaoTurno
from .acao_turno_types import ResultadoAcao


class AcaoComprarCartas(AcaoTurno):
    """
    Ação concreta: Comprar cartas do baralho.

    GoF Template Method Pattern: Concrete Class
    """

    def __init__(self, jogo: 'Jogo', jogador_id: str, cartas_selecionadas: List[str]):
        super().__init__(jogo, jogador_id)
        self.cartas_selecionadas = cartas_selecionadas

    def validar_acao_especifica(self) -> ResultadoAcao:
        """Valida se pode comprar cartas"""

        if len(self.cartas_selecionadas) > 2:
            return ResultadoAcao(
                sucesso=False,
                mensagem="Pode comprar no máximo 2 cartas por turno",
                erros=["LIMITE_CARTAS_EXCEDIDO"]
            )

        return ResultadoAcao(sucesso=True, mensagem="Validação específica OK")

    def executar_acao_especifica(self) -> ResultadoAcao:
        """Executa compra de cartas"""

        cartas_compradas = []

        for carta_id in self.cartas_selecionadas:
            # Lógica de comprar carta (simplificada)
            carta = self.jogo.comprar_carta(carta_id)
            if carta:
                self.jogador.comprarCartaVagao(carta)
                cartas_compradas.append(carta.id)

        return ResultadoAcao(
            sucesso=True,
            mensagem=f"Compradas {len(cartas_compradas)} cartas",
            dados={"cartas_compradas": cartas_compradas}
        )


class AcaoConquistarRota(AcaoTurno):
    """
    Ação concreta: Conquistar rota no tabuleiro.

    GoF Template Method Pattern: Concrete Class
    """

    def __init__(self, jogo: 'Jogo', jogador_id: str, rota_id: str, cartas_usadas: List[str]):
        super().__init__(jogo, jogador_id)
        self.rota_id = rota_id
        self.cartas_usadas = cartas_usadas

    def validar_acao_especifica(self) -> ResultadoAcao:
        """Valida se pode conquistar rota"""

        rota = self.jogo.obter_rota(self.rota_id)
        if not rota:
            return ResultadoAcao(
                sucesso=False,
                mensagem="Rota não encontrada",
                erros=["ROTA_NAO_ENCONTRADA"]
            )

        if rota.proprietario:
            return ResultadoAcao(
                sucesso=False,
                mensagem="Rota já conquistada",
                erros=["ROTA_JA_CONQUISTADA"]
            )

        return ResultadoAcao(sucesso=True, mensagem="Validação específica OK")

    def executar_acao_especifica(self) -> ResultadoAcao:
        """Executa conquista de rota"""

        rota = self.jogo.obter_rota(self.rota_id)

        # Conquista rota (integra com tasks anteriores)
        sucesso = rota.reivindicarRota(self.jogador, self.cartas_usadas)

        if sucesso:
            # Adiciona pontos (integra com Observer Pattern - Task #93)
            pontos = self.jogo.placar.adicionar_pontos_rota(
                self.jogador_id,
                rota.comprimento,
                f"{rota.cidadeA.nome}-{rota.cidadeB.nome}"
            )

            return ResultadoAcao(
                sucesso=True,
                mensagem=f"Rota conquistada! +{pontos} pontos",
                dados={
                    "rota_id": self.rota_id,
                    "pontos_ganhos": pontos
                }
            )
        else:
            return ResultadoAcao(
                sucesso=False,
                mensagem="Falha ao conquistar rota",
                erros=["FALHA_CONQUISTA"]
            )


class AcaoPassarTurno(AcaoTurno):
    """
    Ação concreta: Passar turno sem fazer nada.

    GoF Template Method Pattern: Concrete Class
    """

    def validar_acao_especifica(self) -> ResultadoAcao:
        """Passar turno não requer validações específicas"""
        return ResultadoAcao(sucesso=True, mensagem="Validação específica OK")

    def executar_acao_especifica(self) -> ResultadoAcao:
        """Executa passar turno"""
        return ResultadoAcao(
            sucesso=True,
            mensagem="Turno passado",
            dados={}
        )