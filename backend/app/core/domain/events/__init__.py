"""
Sistema de eventos para conquista de rotas.

GoF Pattern: Observer
- Desacopla ações pós-conquista do executor principal
- Permite adicionar novos handlers sem modificar código existente

GRASP Principles:
- Low Coupling: Observers não conhecem uns aos outros
- Protected Variations: Novos comportamentos via novos observers

Uso típico:
    publisher = ConquestEventPublisher()
    publisher.subscribe(ScoreObserver(placar))
    publisher.subscribe(GameEndObserver(gerenciador_fim))
    
    evento = ConquestEvent(jogador, rota, pontos, trens)
    publisher.publish(evento)  # Notifica todos os observers

Ou usando o orquestrador (recomendado):
    orchestrator = ConquestEventOrchestrator(publisher)
    game_end_observer = orchestrator.publicar_evento_conquista(
        jogo, jogador, rota, resultado_conquista
    )
"""

# Importa de arquivos separados (evita circular imports)
from .conquest_event import ConquestEvent
from .conquest_event_publisher import ConquestEventPublisher, ConquestObserver
from .conquest_event_orchestrator import ConquestEventOrchestrator

# Re-exporta para compatibilidade
__all__ = [
    'ConquestEvent',
    'ConquestEventPublisher',
    'ConquestObserver',
    'ConquestEventOrchestrator',
]
