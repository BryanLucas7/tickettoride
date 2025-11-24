"""
Service para conquista de rotas

GRASP Principles:
- Pure Fabrication: Serviço criado para extrair lógica de conquista de rotas
- High Cohesion: Responsável apenas por conquista de rotas
- Low Coupling: Desacoplado dos routes, pode ser reutilizado
- Controller: Orquestra validação de cartas, conquista e passagem de turno
"""

from typing import List, Dict, Any
from fastapi import HTTPException

from ..core.domain.entities.jogo import Jogo
from ..core.domain.entities.jogador import Jogador
from ..core.domain.entities.rota import Rota
from ..core.domain.entities.carta_vagao import CartaVagao
from ..core.domain.managers.descarte_manager import DescarteManager
from ..core.services.conquista_rota_controller import ConquistaRotaController
from ..services.game_action_service import GameActionService
from ..shared.validators import GameValidators
from ..shared.exception_handlers import handle_validation_errors


class RouteConquestService:
    """
    Serviço responsável por conquista de rotas.
    
    Coordena busca de cartas, validação, conquista via controller
    e passagem de turno automática.
    """
    
    def __init__(self, game_action_service: GameActionService = None):
        """
        Inicializa o serviço.
        
        Args:
            game_action_service: Service para passar turno e verificar fim
        """
        self.game_action_service = game_action_service or GameActionService()
    
    @handle_validation_errors
    def conquistar_rota(
        self,
        jogo: Jogo,
        jogador: Jogador,
        rota_id: str,
        cartas_usadas_cores: List[str]
    ) -> Dict[str, Any]:
        """
        Conquista uma rota no tabuleiro.
        
        Args:
            jogo: Instância do jogo
            jogador: Jogador que está conquistando
            rota_id: ID da rota a ser conquistada
            cartas_usadas_cores: Lista de cores das cartas usadas (strings)
            
        Returns:
            Dicionário com resultado da conquista e informações de turno
            
        Raises:
            HTTPException: Se rota não existir, cartas forem inválidas, etc.
        """
        # 1. Buscar rota pelo ID usando validador centralizado
        rota = GameValidators.buscar_rota(jogo, rota_id)
        
        # 2. Buscar e remover cartas da mão do jogador usando método encapsulado
        cartas_usadas = jogador.mao.remover_cartas_por_cores(cartas_usadas_cores)
        
        # 3. Executar conquista via controller
        resultado_conquista = self._executar_conquista(jogo, jogador, rota, cartas_usadas)
        
        # 4. Passar turno automaticamente (conquista é ação completa)
        resultado_turno = self.game_action_service.passar_turno_e_verificar_fim(jogo)
        
        # 5. Retornar resultado consolidado
        return self._formatar_resposta(resultado_conquista, resultado_turno)
    
    def _executar_conquista(
        self,
        jogo: Jogo,
        jogador: Jogador,
        rota: Rota,
        cartas_usadas: List[CartaVagao]
    ) -> Dict[str, Any]:
        """
        Executa a conquista da rota via controller.
        
        Args:
            jogo: Instância do jogo
            jogador: Jogador conquistando
            rota: Rota a conquistar
            cartas_usadas: Cartas usadas na conquista
            
        Returns:
            Resultado da conquista
            
        Raises:
            HTTPException: Se conquista falhar
        """
        # Garantir que descarte manager existe
        descarte_manager = jogo.descarteManager or DescarteManager()
        
        # Obter ou criar gerenciador de fim de jogo (método movido para Jogo)
        gerenciador_fim_jogo = jogo.obter_ou_criar_gerenciador_fim()
        
        # Criar controller e executar conquista
        controller = ConquistaRotaController(
            descarte_manager=descarte_manager,
            validador_duplas=getattr(jogo.tabuleiro, 'validador_duplas', None),
            placar=jogo.placar,
            gerenciador_fim_jogo=gerenciador_fim_jogo
        )
        
        resultado = controller.conquistar_rota(
            jogador=jogador,
            rota=rota,
            cartas_usadas=cartas_usadas,
            total_jogadores=len(jogo.gerenciadorDeTurnos.jogadores)
        )
        
        # Resultado já vem no formato correto (success/message) do controller
        resultado_normalizado = resultado
        
        if not resultado_normalizado["success"]:
            raise HTTPException(status_code=400, detail=resultado_normalizado["message"])
        
        return resultado
    
    def _formatar_resposta(
        self,
        resultado_conquista: Dict[str, Any],
        resultado_turno: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Formata resposta consolidada.
        
        Args:
            resultado_conquista: Resultado da conquista
            resultado_turno: Resultado da passagem de turno
            
        Returns:
            Dicionário formatado para resposta da API
        """
        from ..shared.response_builder import ResponseBuilder
        
        return ResponseBuilder.success_with_turn(
            message=resultado_conquista["mensagem"],
            resultado_turno=resultado_turno,
            points=resultado_conquista.get("pontos_ganhos", 0),
            trains_remaining=resultado_conquista.get("trens_restantes", 0),
            game_ending=resultado_conquista.get("fim_de_jogo_ativado", False)
        )
