"""
Observers para eventos de conquista de rota.

SRP: Cada observer tem uma única responsabilidade:
- ScoreObserver: Registrar pontos no placar
- GameEndObserver: Verificar condição de fim de jogo
- LoggingObserver: Registrar logs (opcional)

GoF Pattern: Observer
- Implementações concretas da interface ConquestObserver
"""

import logging
from typing import Optional

from .conquest_event import ConquestEvent
from .conquest_event_publisher import ConquestObserver
from ..calculators.placar import Placar
from ..managers.gerenciador_fim_jogo import GerenciadorFimDeJogo

logger = logging.getLogger(__name__)


class ScoreObserver(ConquestObserver):
    """
    Observer responsável por registrar pontos no placar.
    
    SRP: Única responsabilidade - atualizar pontuação após conquista.
    
    Quando notificado de uma conquista:
    1. Calcula pontos baseado no comprimento da rota
    2. Adiciona pontos ao placar do jogador
    3. Loga a operação
    """
    
    def __init__(self, placar: Placar):
        """
        Inicializa com referência ao placar.
        
        Args:
            placar: Placar do jogo onde pontos serão registrados
        """
        self._placar = placar
    
    def on_conquest(self, event: ConquestEvent) -> None:
        """
        Registra pontos da conquista no placar.
        
        Args:
            event: Dados do evento de conquista
        """
        if self._placar is None:
            logger.warning("⚠️ ScoreObserver: Placar não configurado, ignorando")
            return
        
        self._placar.adicionar_pontos_rota(
            jogador_id=event.jogador.id,
            comprimento_rota=event.rota.comprimento,
            nome_rota=event.nome_rota
        )
        logger.info(f"📊 Pontos registrados: {event.pontos_ganhos} para {event.jogador.nome}")


class GameEndObserver(ConquestObserver):
    """
    Observer responsável por verificar condição de fim de jogo.
    
    SRP: Única responsabilidade - verificar e sinalizar fim de jogo.
    
    Quando notificado de uma conquista:
    1. Verifica se jogador atingiu limite de trens
    2. Atualiza estado de fim de jogo se necessário
    3. Armazena mensagem de alerta
    
    Após processar, verificar:
        observer.fim_ativado  # True se fim foi ativado
        observer.mensagem_fim  # Mensagem de alerta
    """
    
    def __init__(self, gerenciador_fim: GerenciadorFimDeJogo):
        """
        Inicializa com referência ao gerenciador de fim.
        
        Args:
            gerenciador_fim: Gerenciador que controla condição de fim
        """
        self._gerenciador_fim = gerenciador_fim
        self.fim_ativado: bool = False
        self.mensagem_fim: Optional[str] = None
    
    def on_conquest(self, event: ConquestEvent) -> None:
        """
        Verifica se conquista ativou fim de jogo.
        
        Args:
            event: Dados do evento de conquista
        """
        if self._gerenciador_fim is None:
            logger.warning("⚠️ GameEndObserver: Gerenciador não configurado, ignorando")
            return
        
        estado_fim = self._gerenciador_fim.verificar_condicao_fim(
            jogador_id=event.jogador.id,
            trens_restantes=event.trens_restantes
        )
        
        self.fim_ativado = estado_fim.get("fim_ativado", False)
        self.mensagem_fim = estado_fim.get("mensagem")
        
        if self.fim_ativado:
            logger.info(f"🏁 Fim de jogo ativado: {self.mensagem_fim}")
    
    def reset(self) -> None:
        """Reseta estado (útil para reutilização)."""
        self.fim_ativado = False
        self.mensagem_fim = None


class LoggingObserver(ConquestObserver):
    """
    Observer para logging de conquistas (opcional).
    
    SRP: Única responsabilidade - registrar logs detalhados.
    Útil para debug e auditoria.
    """
    
    def __init__(self, log_level: int = logging.INFO):
        """
        Inicializa com nível de log desejado.
        
        Args:
            log_level: Nível de logging (INFO, DEBUG, etc)
        """
        self._log_level = log_level
    
    def on_conquest(self, event: ConquestEvent) -> None:
        """
        Registra log detalhado da conquista.
        
        Args:
            event: Dados do evento de conquista
        """
        logger.log(
            self._log_level,
            f"🎯 Conquista: {event.jogador.nome} conquistou {event.nome_rota} "
            f"(+{event.pontos_ganhos} pts, {event.trens_restantes} trens restantes)"
        )
