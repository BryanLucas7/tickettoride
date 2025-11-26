"""
Placar - Gerenciador de pontuação dos jogadores.

Implementa Observer Pattern para notificar mudanças de pontuação.

GoF Pattern: Observer Pattern
- Subject: Placar (notifica observers quando pontos mudam)
- Observer: PontuacaoObserver (interface em pontuacao_observer.py)

GRASP Principles Applied:
- Information Expert: Placar calcula pontos baseado em comprimento
- Low Coupling: Observers desacoplados do Subject
- Protected Variations: Tabela de pontos encapsulada

Design Decisions:
- Tabela de pontos: {1→1, 2→2, 3→4, 4→7, 5→10, 6→15}
- Observers notificados quando pontos mudam
- Suporta múltiplos observers simultâneos

Refatoração SRP:
- PontuacaoObserver (interface) extraída para pontuacao_observer.py
- LogPontuacaoObserver, HistoricoPontuacaoObserver extraídos para pontuacao_observers.py
"""

from dataclasses import dataclass, field
from typing import List, Dict
from app.constants import TABELA_PONTOS_ROTA

# Importa interface e implementações concretas dos arquivos separados (SRP)
from .pontuacao_observer import PontuacaoObserver
from .pontuacao_observers import LogPontuacaoObserver, HistoricoPontuacaoObserver

# Re-exporta para compatibilidade com código existente
__all__ = ['Placar', 'PontuacaoObserver', 'LogPontuacaoObserver', 'HistoricoPontuacaoObserver']


@dataclass
class Placar:
    """
    Gerencia pontuação dos jogadores e notifica observers.
    
    GoF Observer Pattern: Subject
    GRASP Information Expert: Conhece tabela de pontos e calcula pontuação
    GRASP Protected Variations: Tabela de pontos encapsulada
    
    Attributes:
        jogadores: Lista de jogadores
        pontuacoes: Dict mapeando jogador_id → pontos
        observers: Lista de observers registrados
    """
    
    jogadores: List = field(default_factory=list)
    pontuacoes: Dict[str, int] = field(default_factory=dict)
    _observers: List[PontuacaoObserver] = field(default_factory=list, repr=False)
    
    def registrar_observer(self, observer: PontuacaoObserver):
        """Registra um observer para receber notificações
        
        GoF Observer Pattern: attach()
        """
        if observer not in self._observers:
            self._observers.append(observer)
    
    def remover_observer(self, observer: PontuacaoObserver):
        """Remove um observer
        
        GoF Observer Pattern: detach()
        """
        if observer in self._observers:
            self._observers.remove(observer)
    
    def _notificar_observers(self, jogador_id: str, pontos_adicionados: int, motivo: str):
        """Notifica todos os observers sobre mudança de pontuação
        
        GoF Observer Pattern: notify()
        """
        pontos_atuais = self.pontuacoes.get(jogador_id, 0)
        for observer in self._observers:
            observer.atualizar_pontuacao(jogador_id, pontos_atuais, pontos_adicionados, motivo)
    
    def calcular_pontos_rota(self, comprimento: int) -> int:
        """Calcula pontos baseado no comprimento da rota
        
        GRASP Information Expert: Placar conhece tabela de pontos
        GRASP Protected Variations: Tabela protegida de mudanças
        
        Args:
            comprimento: Comprimento da rota (1-6)
            
        Returns:
            Pontos ganhos pela rota
        """
        return TABELA_PONTOS_ROTA.get(comprimento, 0)
    
    def adicionar_pontos_rota(self, jogador_id: str, comprimento_rota: int, 
                             nome_rota: str = "") -> int:
        """Adiciona pontos por rota conquistada
        
        Args:
            jogador_id: ID do jogador
            comprimento_rota: Comprimento da rota
            nome_rota: Nome descritivo da rota (opcional)
            
        Returns:
            Quantidade de pontos adicionados
        """
        pontos = self.calcular_pontos_rota(comprimento_rota)
        
        if jogador_id not in self.pontuacoes:
            self.pontuacoes[jogador_id] = 0
        
        self.pontuacoes[jogador_id] += pontos
        
        # Notifica observers
        motivo = nome_rota if nome_rota else f"Rota de {comprimento_rota} espaços"
        self._notificar_observers(jogador_id, pontos, motivo)
        
        return pontos
    
    def adicionar_pontos_customizado(self, jogador_id: str, pontos: int, motivo: str):
        """Adiciona pontos customizados (ex: bilhetes, maior caminho)
        
        Args:
            jogador_id: ID do jogador
            pontos: Quantidade de pontos (pode ser negativo)
            motivo: Descrição do motivo
        """
        if jogador_id not in self.pontuacoes:
            self.pontuacoes[jogador_id] = 0
        
        self.pontuacoes[jogador_id] += pontos
        
        # Notifica observers
        self._notificar_observers(jogador_id, pontos, motivo)
    
    def obter_pontuacao(self, jogador_id: str) -> int:
        """Obtém pontuação atual do jogador"""
        return self.pontuacoes.get(jogador_id, 0)
    
    def obter_ranking(self) -> List[tuple]:
        """Obtém ranking de jogadores ordenado por pontos
        
        Returns:
            Lista de tuplas (jogador_id, pontos) ordenada por pontos (maior primeiro)
        """
        return sorted(self.pontuacoes.items(), key=lambda x: x[1], reverse=True)
    
    def resetar(self):
        """Reseta todas as pontuações (para novo jogo)"""
        self.pontuacoes.clear()
    
    def atualizarPlacar(self):
        """Atualiza o placar com as pontuações atuais"""
        for jogador in self.jogadores:
            jogador.pontuacao = self.obter_pontuacao(jogador.id)
