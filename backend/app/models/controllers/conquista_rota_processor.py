"""
Processador de conquista de rotas.

PADRÃO GRASP: Pure Fabrication
- ConquistaRotaProcessor encapsula o processamento físico da conquista
- Separa lógica de processamento do controller
"""

from typing import List, Dict
from ..entities.jogador import Jogador
from ..entities.rota import Rota
from ..entities.carta_vagao import CartaVagao
from ..managers.descarte_manager import DescarteManager
from ..managers.conquista_rota_service import ConquistaRotaService
from ..strategies.validador_rotas_duplas import ValidadorRotasDuplas


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

        if not resultado_conquista["sucesso"]:
            return {
                "sucesso": False,
                "mensagem": resultado_conquista["mensagem"]
            }

        # 2. Processar rota dupla e marcar rota como conquistada
        rota_dupla_bloqueada = False
        if validador_duplas and total_jogadores <= 3:
            resultado_bloqueio = validador_duplas.processar_conquista(rota, jogador)
            rota_dupla_bloqueada = resultado_bloqueio.get('bloqueou_paralela', False)
        else:
            # Se não tem validador duplas, marca manualmente
            rota.reivindicarRota(jogador, cartas_usadas)

        return {
            "sucesso": True,
            "resultado_conquista": resultado_conquista,
            "rota_dupla_bloqueada": rota_dupla_bloqueada
        }