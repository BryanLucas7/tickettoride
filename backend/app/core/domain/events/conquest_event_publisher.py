"""
ConquestEventPublisher - Publisher de eventos de conquista.

GoF Pattern: Observer
- Mantém lista de observers e notifica todos quando evento ocorre
"""

from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .conquest_event import ConquestEvent


class ConquestObserver(ABC):
    """
    Interface para observers de conquista de rota.
    
    GoF Observer Pattern: Define interface comum para todos os observers.
    Cada implementação processa o evento de forma diferente.
    """
    
    @abstractmethod
    def on_conquest(self, event: 'ConquestEvent') -> None:
        """
        Chamado quando uma rota é conquistada.
        
        Args:
            event: Dados do evento de conquista
        """
        pass


class ConquestEventPublisher:
    """
    Publisher de eventos de conquista.
    
    GoF Observer Pattern: Mantém lista de observers e notifica todos
    quando um evento de conquista ocorre.
    
    Responsabilidades:
    - Manter lista de observers registrados
    - Notificar observers quando evento ocorrer
    - Permitir subscribe/unsubscribe dinâmico
    """
    
    def __init__(self):
        """Inicializa com lista vazia de observers."""
        self._observers: List[ConquestObserver] = []
    
    def subscribe(self, observer: ConquestObserver) -> None:
        """
        Registra um observer.
        
        Args:
            observer: Observer a ser notificado em conquistas
        """
        if observer not in self._observers:
            self._observers.append(observer)
    
    def unsubscribe(self, observer: ConquestObserver) -> None:
        """
        Remove um observer.
        
        Args:
            observer: Observer a ser removido
        """
        if observer in self._observers:
            self._observers.remove(observer)
    
    def publish(self, event: 'ConquestEvent') -> None:
        """
        Notifica todos os observers sobre uma conquista.
        
        Args:
            event: Dados do evento de conquista
        """
        for observer in self._observers:
            observer.on_conquest(event)
    
    def clear(self) -> None:
        """Remove todos os observers (útil para testes)."""
        self._observers.clear()
    
    @property
    def observer_count(self) -> int:
        """Retorna número de observers registrados."""
        return len(self._observers)
