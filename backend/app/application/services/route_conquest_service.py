"""
Service para conquista de rotas - Versão Refatorada.

Refatoração SRP: Service agora é apenas um ORQUESTRADOR do pipeline.
Responsabilidades específicas foram extraídas para classes colaboradoras:

- RouteCardValidator: validação de cartas
- ConquestEventOrchestrator: orquestração de eventos (configurar, criar, limpar observers)
- ConquestResponseAssembler: formatação de resposta

REFATORAÇÃO DRY: Usa HttpErrors para exceções HTTP padronizadas.

GRASP Principles:
- Pure Fabrication: Serviço criado para extrair lógica de conquista de rotas
- High Cohesion: Responsável apenas por ORQUESTRAR conquista de rotas
- Low Coupling: Usa injeção de dependência para colaboradores
- Controller: Orquestra o pipeline delegando para especialistas

GoF Patterns:
- Observer: ConquestEventOrchestrator gerencia observers após conquista

Pipeline Steps (orquestração apenas):
1. Buscar rota no tabuleiro
2. Converter cores para cartas
3. Validar cartas (delegado para RouteCardValidator)
4. Executar conquista via controller
5. Publicar evento (delegado para ConquestEventOrchestrator)
6. Passar turno
7. Montar resposta (delegado para ConquestResponseAssembler)
"""

import logging
from typing import List, Dict, Any, Optional

from ...core.domain.entities.jogo import Jogo
from ...core.domain.entities.jogador import Jogador
from ...core.domain.entities.rota import Rota
from ...core.domain.entities.carta_vagao import CartaVagao
from ...core.domain.validators.route_card_validator import RouteCardValidator
from ...core.domain.events import ConquestEventOrchestrator
from ...core.domain.events.conquest_observers import GameEndObserver
from ...core.services.conquista_rota_controller import ConquistaRotaController
from ...shared.assemblers.conquest_response_assembler import ConquestResponseAssembler
from ...shared.carta_converter import CartaConverter
from ...shared.validators import GameValidators
from ...shared.exception_handlers import handle_validation_errors
from ...shared.http_errors import HttpErrors
from .game_action_service import GameActionService

logger = logging.getLogger(__name__)


class RouteConquestService:
    """
    Orquestrador do pipeline de conquista de rotas.
    
    SRP: Apenas COORDENA os steps, delegando responsabilidades:
    - RouteCardValidator: validação de cartas
    - ConquistaRotaController: execução da conquista
    - ConquestEventOrchestrator: orquestração de eventos
    - ConquestResponseAssembler: formatação de resposta
    
    Dependency Injection:
    - Colaboradores são injetáveis via construtor
    - Facilita testes unitários com mocks
    """
    
    def __init__(
        self,
        game_action_service: Optional[GameActionService] = None,
        card_validator: Optional[RouteCardValidator] = None,
        event_orchestrator: Optional[ConquestEventOrchestrator] = None
    ):
        """
        Inicializa com dependências injetadas.
        
        Args:
            game_action_service: Service para ações de jogo (passar turno)
            card_validator: Validador de cartas (injetável para testes)
            event_orchestrator: Orquestrador de eventos (injetável para testes)
        """
        self.game_action_service = game_action_service or GameActionService()
        self.card_validator = card_validator or RouteCardValidator()
        self.event_orchestrator = event_orchestrator or ConquestEventOrchestrator()
    
    @handle_validation_errors
    def conquistar_rota(
        self,
        jogo: Jogo,
        jogador: Jogador,
        rota_id: str,
        cartas_usadas_cores: List[str]
    ) -> Dict[str, Any]:
        """
        Pipeline de conquista de rota.
        
        Steps:
        1. Buscar rota
        2. Converter cartas
        3. Validar cartas (DELEGADO para RouteCardValidator)
        4. Executar conquista
        5. Publicar evento (observers cuidam de pontos e fim de jogo)
        6. Passar turno
        7. Montar resposta (DELEGADO para ConquestResponseAssembler)
        
        Args:
            jogo: Instância do jogo
            jogador: Jogador que está conquistando
            rota_id: ID da rota a ser conquistada
            cartas_usadas_cores: Lista de cores das cartas usadas (strings)
            
        Returns:
            Dicionário com resultado da conquista e informações de turno
        """
        # Step 1: Buscar rota
        rota = self._buscar_rota(jogo, rota_id)
        
        # Step 2: Converter cartas
        cartas_usadas = self._converter_cartas(jogador, cartas_usadas_cores)
        
        # Step 3: Validar cartas (DELEGADO para RouteCardValidator)
        self._validar_cartas(rota, cartas_usadas)
        
        # Step 4: Executar conquista
        resultado_conquista = self._executar_conquista(jogo, jogador, rota, cartas_usadas)
        
        # Step 5: Publicar evento (DELEGADO para ConquestEventOrchestrator)
        game_end_observer = self.event_orchestrator.publicar_evento_conquista(
            jogo, jogador, rota, resultado_conquista
        )
        
        # Step 6: Passar turno
        resultado_turno = self.game_action_service.passar_turno_e_verificar_fim(jogo)
        
        # Step 7: Montar resposta (DELEGADO para ConquestResponseAssembler)
        return ConquestResponseAssembler.montar_sucesso(
            mensagem=resultado_conquista["message"],
            resultado_turno=resultado_turno,
            pontos_ganhos=resultado_conquista.get("pontos_ganhos", 0),
            trens_restantes=resultado_conquista.get("trens_restantes", 0),
            fim_de_jogo_ativado=game_end_observer.fim_ativado if game_end_observer else False,
            alerta_fim_jogo=game_end_observer.mensagem_fim if game_end_observer else None
        )
    
    # === Pipeline Steps ===
    
    def _buscar_rota(self, jogo: Jogo, rota_id: str) -> Rota:
        """
        Step 1: Localiza rota no tabuleiro.
        
        Delega para GameValidators que já centraliza essa busca.
        """
        rota = GameValidators.buscar_rota(jogo, rota_id)
        logger.info(f"🔍 Rota encontrada: {rota_id}")
        return rota
    
    def _converter_cartas(
        self, 
        jogador: Jogador, 
        cartas_cores: List[str]
    ) -> List[CartaVagao]:
        """
        Step 2: Converte cores para objetos CartaVagao.
        
        Delega para CartaConverter que já centraliza essa conversão.
        REFATORAÇÃO DRY: Usa HttpErrors para exceções padronizadas.
        """
        cartas_usadas, erro = CartaConverter.converter_cores_para_cartas(
            jogador, cartas_cores
        )
        if erro:
            logger.error(f"❌ {erro}")
            raise HttpErrors.bad_request(erro)
        
        logger.info(f"✅ Cartas identificadas: {len(cartas_usadas)} cartas")
        return cartas_usadas
    
    def _validar_cartas(self, rota: Rota, cartas_usadas: List[CartaVagao]) -> None:
        """
        Step 3: Valida compatibilidade cartas-rota.
        
        DELEGADO para RouteCardValidator (SRP).
        REFATORAÇÃO DRY: Usa HttpErrors para exceções padronizadas.
        """
        resultado = self.card_validator.validar(rota, cartas_usadas)
        if resultado.invalido:
            logger.error(f"❌ Validação falhou: {resultado.erro}")
            raise HttpErrors.bad_request(resultado.erro)
        
        logger.info(f"✅ Cartas validadas para rota {rota.id}")
    
    def _executar_conquista(
        self,
        jogo: Jogo,
        jogador: Jogador,
        rota: Rota,
        cartas_usadas: List[CartaVagao]
    ) -> Dict[str, Any]:
        """
        Step 4: Executa conquista via controller.
        
        Controller é responsável pela lógica de conquista:
        - Marcar rota como conquistada
        - Remover cartas do jogador
        - Calcular pontos
        
        REFATORAÇÃO DRY: Usa HttpErrors para exceções padronizadas.
        """
        controller = ConquistaRotaController()
        
        logger.info(f"🔄 Executando conquista: {jogador.nome} → {rota.id}")
        
        try:
            resultado = controller.conquistar_rota(
                jogador=jogador,
                rota=rota,
                cartas_usadas=cartas_usadas,
                total_jogadores=len(jogo.gerenciadorDeTurnos.jogadores),
                validador_duplas=getattr(jogo.tabuleiro, 'validador_duplas', None)
            )
        except Exception as e:
            logger.error(f"💥 Erro no controller: {e}")
            raise HttpErrors.bad_request(f"Erro ao conquistar rota: {str(e)}")
        
        if not resultado["success"]:
            raise HttpErrors.bad_request(resultado["message"])
        
        logger.info(f"✅ Conquista executada: {resultado['message']}")
        return resultado
