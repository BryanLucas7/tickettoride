"""
Processador de conquista de rotas.

PADRÃO GRASP: Pure Fabrication
- ConquistaRotaProcessor encapsula o processamento físico da conquista
- Separa lógica de processamento do controller
"""

from typing import List, Dict
from ..domain.entities.jogador import Jogador
from ..domain.entities.rota import Rota
from ..domain.entities.carta_vagao import CartaVagao
from ..domain.managers.descarte_manager import DescarteManager
from ..domain.managers.conquista_rota_service import ConquistaRotaService
from ..domain.strategies.validador_rotas_duplas import ValidadorRotasDuplas
from ..domain.support.responses import (
    success_response,
    error_response,
    normalize_result,
)


class ConquistaRotaProcessor:
    """
    Pure Fabrication - Processa a conquista física de rotas.

    Responsabilidades:
    - Executar descarte de cartas e remoção de trens
    - Marcar rota como conquistada
    - Processar regras de rotas duplas
    - Retornar resultado do processamento

    GRASP Principles:
    - Pure Fabrication: Classe criada para responsabilidade específica
    - Information Expert: Conhece processo de conquista
    - Low Coupling: Recebe dependências por parâmetro
    - High Cohesion: Focado apenas em processamento
    """

    def __init__(self, descarte_manager: DescarteManager = None):
        """
        Inicializa o processador.

        Args:
            descarte_manager: Gerenciador de descarte (opcional)
        """
        self.descarte_manager = descarte_manager or DescarteManager()

    def processar_conquista(
        self,
        jogador: Jogador,
        rota: Rota,
        cartas_usadas: List[CartaVagao],
        validador_duplas: ValidadorRotasDuplas = None,
        total_jogadores: int = 0
    ) -> Dict:
        """
        Processa a conquista física da rota.

        Args:
            jogador: Jogador conquistando
            rota: Rota sendo conquistada
            cartas_usadas: Cartas usadas
            validador_duplas: Validador de rotas duplas (opcional)
            total_jogadores: Total de jogadores (para regras duplas)

        Returns:
            Dict com resultado do processamento
        """
        # 1. Processar conquista física (descarte, trens)
        resultado_conquista = ConquistaRotaService.conquistar_rota(
            jogador=jogador,
            rota=rota,
            cartas_usadas=cartas_usadas,
            descarte_manager=self.descarte_manager
        )

        # Normaliza resposta de formato legado (português) para padrão (inglês)
        resultado_normalizado = normalize_result(resultado_conquista)

        if not resultado_normalizado["success"]:
            return error_response(resultado_normalizado["message"])

        # 2. Processar rota dupla e marcar rota como conquistada
        rota_dupla_bloqueada = False
        if validador_duplas and total_jogadores <= 3:
            resultado_bloqueio = validador_duplas.processar_conquista(rota, jogador)
            rota_dupla_bloqueada = resultado_bloqueio.get('bloqueou_paralela', False)
        else:
            # Se não tem validador duplas, marca manualmente
            rota.reivindicarRota(jogador, cartas_usadas)

        return success_response(
            "Conquista processada com sucesso",
            resultado_conquista=resultado_conquista,
            rota_dupla_bloqueada=rota_dupla_bloqueada
        )