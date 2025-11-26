"""
ConquestEventOrchestrator - Orquestrador de eventos de conquista.

SRP: Responsável APENAS por configurar, criar e gerenciar eventos de conquista.
Extraído de RouteConquestService para melhorar separação de responsabilidades.

Padrão GRASP: Pure Fabrication
- Classe criada para extrair responsabilidade de orquestração de eventos
"""

from typing import Dict, Any, Optional, Tuple

from ..entities.jogo import Jogo
from ..entities.jogador import Jogador
from ..entities.rota import Rota
from .conquest_event import ConquestEvent
from .conquest_event_publisher import ConquestEventPublisher
from .conquest_observers import ScoreObserver, GameEndObserver


class ConquestEventOrchestrator:
    """
    Orquestra configuração, criação e limpeza de eventos de conquista.
    
    SRP: Única responsabilidade - gerenciar ciclo de vida dos eventos.
    
    Responsabilidades:
    - Configurar observers necessários
    - Criar eventos de conquista
    - Publicar eventos
    - Limpar observers após publicação
    
    Exemplo de uso:
        orchestrator = ConquestEventOrchestrator(event_publisher)
        game_end_observer = orchestrator.publicar_evento_conquista(
            jogo, jogador, rota, resultado_conquista
        )
    """
    
    def __init__(self, event_publisher: Optional[ConquestEventPublisher] = None):
        """
        Inicializa o orquestrador com publisher de eventos.
        
        Args:
            event_publisher: Publisher de eventos (injetável para testes)
        """
        self.event_publisher = event_publisher or ConquestEventPublisher()
    
    def publicar_evento_conquista(
        self,
        jogo: Jogo,
        jogador: Jogador,
        rota: Rota,
        resultado_conquista: Dict[str, Any]
    ) -> Optional[GameEndObserver]:
        """
        Configura observers, publica evento e limpa observers.
        
        Pipeline:
        1. Configurar observers necessários
        2. Criar evento de conquista
        3. Publicar evento
        4. Limpar observers
        
        Args:
            jogo: Instância do jogo
            jogador: Jogador que conquistou a rota
            rota: Rota conquistada
            resultado_conquista: Resultado da conquista com pontos e trens
            
        Returns:
            GameEndObserver para acessar estado de fim de jogo
        """
        # Step 1: Configurar observers
        score_observer, game_end_observer = self._configurar_observers(jogo)
        
        # Step 2: Criar evento
        evento = self._criar_evento_conquista(jogador, rota, resultado_conquista)
        
        # Step 3: Publicar evento
        self.event_publisher.publish(evento)
        
        # Step 4: Limpar observers
        self._limpar_observers(score_observer, game_end_observer)
        
        return game_end_observer
    
    def _configurar_observers(
        self, 
        jogo: Jogo
    ) -> Tuple[Optional[ScoreObserver], Optional[GameEndObserver]]:
        """
        Configura observers para o evento de conquista.
        
        SRP: Única responsabilidade - configurar observers.
        
        Args:
            jogo: Instância do jogo
            
        Returns:
            Tupla (ScoreObserver, GameEndObserver) - pode ser None se não aplicável
        """
        score_observer = None
        game_end_observer = None
        
        # Configurar ScoreObserver se houver placar
        if jogo.estado.placar:
            score_observer = ScoreObserver(jogo.estado.placar)
            self.event_publisher.subscribe(score_observer)
        
        # Configurar GameEndObserver
        gerenciador_fim = jogo.obter_ou_criar_gerenciador_fim()
        if gerenciador_fim:
            game_end_observer = GameEndObserver(gerenciador_fim)
            self.event_publisher.subscribe(game_end_observer)
        
        return score_observer, game_end_observer
    
    def _criar_evento_conquista(
        self,
        jogador: Jogador,
        rota: Rota,
        resultado_conquista: Dict[str, Any]
    ) -> ConquestEvent:
        """
        Cria evento de conquista de rota.
        
        SRP: Única responsabilidade - criar evento.
        
        Args:
            jogador: Jogador que conquistou
            rota: Rota conquistada
            resultado_conquista: Resultado da conquista
            
        Returns:
            ConquestEvent configurado
        """
        return ConquestEvent(
            jogador=jogador,
            rota=rota,
            pontos_ganhos=resultado_conquista.get("pontos_ganhos", 0),
            trens_restantes=resultado_conquista.get("trens_restantes", 0)
        )
    
    def _limpar_observers(
        self,
        score_observer: Optional[ScoreObserver],
        game_end_observer: Optional[GameEndObserver]
    ) -> None:
        """
        Remove observers após publicação do evento.
        
        SRP: Única responsabilidade - cleanup de observers.
        Evita acúmulo de observers entre chamadas.
        
        Args:
            score_observer: Observer de pontuação (ou None)
            game_end_observer: Observer de fim de jogo (ou None)
        """
        if score_observer:
            self.event_publisher.unsubscribe(score_observer)
        if game_end_observer:
            self.event_publisher.unsubscribe(game_end_observer)
