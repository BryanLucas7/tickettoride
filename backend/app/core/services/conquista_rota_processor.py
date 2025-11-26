"""
Processador de conquista de rotas.

PADRÃO GRASP: Pure Fabrication
- ConquistaRotaProcessor encapsula o processamento físico da conquista
- Separa lógica de processamento do controller

REFATORAÇÃO DRY: ConquistaRotaService foi integrado diretamente aqui
para eliminar camada extra de indireção. A lógica é simples o suficiente
para ficar em um único local.
"""

from typing import List, Dict
from ..domain.entities.jogador import Jogador
from ..domain.entities.rota import Rota
from ..domain.entities.carta_vagao import CartaVagao
from ..domain.managers.descarte_manager import DescarteManager
from ..domain.strategies.rota_dupla_processor import RotaDuplaProcessor
from ..domain.support.responses import (
    success_response,
    error_response,
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
    
    REFATORAÇÃO DRY: Integra lógica que estava em ConquistaRotaService
    para eliminar indireção desnecessária.
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
        validador_duplas: RotaDuplaProcessor = None,
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
        # 1. Processar conquista física (descarte, trens) - INLINE de ConquistaRotaService
        resultado_conquista = self._executar_conquista_fisica(
            jogador=jogador,
            rota=rota,
            cartas_usadas=cartas_usadas
        )

        if not resultado_conquista["success"]:
            return error_response(resultado_conquista["message"])

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
    
    def _executar_conquista_fisica(
        self,
        jogador: Jogador,
        rota: Rota,
        cartas_usadas: List[CartaVagao]
    ) -> Dict:
        """
        Executa conquista física: descarte de cartas e remoção de trens.
        
        REFATORAÇÃO DRY: Lógica movida de ConquistaRotaService para cá.
        
        Args:
            jogador: Jogador conquistando
            rota: Rota sendo conquistada
            cartas_usadas: Cartas a descartar
            
        Returns:
            Dict com resultado da operação
        """
        trens_necessarios = rota.comprimento
        
        # 1. Valida se jogador tem trens suficientes
        if len(jogador.vagoes) < trens_necessarios:
            return error_response(
                f"Trens insuficientes: tem {len(jogador.vagoes)}, precisa de {trens_necessarios}",
                cartas_descartadas=0,
                trens_removidos=0,
                trens_restantes=len(jogador.vagoes)
            )
        
        # 2. Valida se jogador tem as cartas usadas
        for carta in cartas_usadas:
            if carta not in jogador.mao.cartasVagao:
                return error_response(
                    "Carta não encontrada na mão do jogador",
                    cartas_descartadas=0,
                    trens_removidos=0,
                    trens_restantes=len(jogador.vagoes)
                )
        
        # 3. Remove cartas da mão do jogador para evitar duplicidade
        sucesso_remocao = jogador.removerCartasVagao(cartas_usadas)
        if not sucesso_remocao:
            return error_response(
                "Falha ao remover cartas da mão",
                cartas_descartadas=0,
                trens_removidos=0,
                trens_restantes=len(jogador.vagoes)
            )
        
        # 4. Descarta cartas usadas
        qtd_descartada = self.descarte_manager.descartar_cartas(cartas_usadas)
        
        # 5. Remove trens do jogador
        trens_removidos = 0
        for _ in range(trens_necessarios):
            if jogador.vagoes:
                jogador.vagoes.pop()
                trens_removidos += 1
        
        return success_response(
            f"Rota conquistada! Descartadas {qtd_descartada} cartas, removidos {trens_removidos} trens",
            cartas_descartadas=qtd_descartada,
            trens_removidos=trens_removidos,
            trens_restantes=len(jogador.vagoes)
        )