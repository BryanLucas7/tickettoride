"""

Implementa Observer Pattern para notificar mudanças de pontuação.

GoF Pattern: Observer Pattern
- Subject: Placar (notifica observers quando pontos mudam)
- Observer: Interface para observers (PlacarObserver, UIObserver)

GRASP Principles Applied:
- Information Expert: Placar calcula pontos baseado em comprimento
- Low Coupling: Observers desacoplados do Subject
- Protected Variations: Tabela de pontos encapsulada

Design Decisions:
- Tabela de pontos: {1→1, 2→2, 3→4, 4→7, 5→10, 6→15}
- Observers notificados quando pontos mudam
- Suporta múltiplos observers simultâneos
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict


# TABELA DE PONTUAÇÃO (Protected Variations)
TABELA_PONTOS_ROTA = {
    1: 1,
    2: 2,
    3: 4,
    4: 7,
    5: 10,
    6: 15,
}


class PontuacaoObserver(ABC):
    """
    Interface Observer para notificações de mudança de pontuação.
    
    GoF Observer Pattern: Interface Observer
    """
    
    @abstractmethod
    def atualizar_pontuacao(self, jogador_id: str, pontos_atuais: int, 
                           pontos_adicionados: int, motivo: str):
        """Notificação de mudança de pontuação
        
        Args:
            jogador_id: ID do jogador
            pontos_atuais: Pontuação total atual
            pontos_adicionados: Quantidade de pontos adicionados (ou subtraídos se negativo)
            motivo: Descrição da razão da mudança (ex: "Rota Los Angeles - Seattle")
        """
        pass


@dataclass
class Placar:
    """
    Gerencia pontuação dos jogadores e notifica observers.
    
    GoF Observer Pattern: Subject
    GRASP Information Expert: Conhece tabela de pontos e calcula pontuação
    GRASP Protected Variations: Tabela de pontos encapsulada
    
    Attributes:
        jogadores: Lista de jogadores (mantida para compatibilidade)
        pontuacoes: Dict mapeando jogador_id → pontos
        observers: Lista de observers registrados
    """
    
    jogadores: List = field(default_factory=list)  # Compatibilidade
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
    
    # ============ MÉTODOS LEGADOS (compatibilidade) ============
    
    def calcularPontuacaoAtualJogador(self, jogador) -> int:
        """Calcula a pontuação atual de um jogador (sem bilhetes)"""
        return self.obter_pontuacao(jogador.id)

    def calcularPontuacaoFinalJogador(self, jogador) -> int:
        """Calcula a pontuação final de um jogador (incluindo bilhetes)"""
        total = self.obter_pontuacao(jogador.id)
        
        # Adiciona pontos de bilhetes concluídos
        for bilhete in jogador.bilhetes:
            # TODO: Verificar se o bilhete foi realmente concluído
            # Por enquanto, assume que todos foram concluídos
            total += bilhete.pontos
        
        return total

    def atualizarPlacar(self):
        """Atualiza o placar com as pontuações atuais"""
        # Recalcula pontuações de todos os jogadores
        for jogador in self.jogadores:
            jogador.pontuacao = self.obter_pontuacao(jogador.id)

    def getVencedor(self):
        """Retorna o jogador vencedor"""
        if not self.jogadores:
            return None
        
        pontuacoes = {j: self.calcularPontuacaoFinalJogador(j) for j in self.jogadores}
        vencedor = max(pontuacoes, key=pontuacoes.get)
        return vencedor


# ==================== OBSERVERS CONCRETOS ====================

@dataclass(eq=False)  # Comparação por identidade, não por valor
class LogPontuacaoObserver(PontuacaoObserver):
    """
    Observer que loga mudanças de pontuação no console.
    
    GoF Observer Pattern: Concrete Observer
    Útil para debug e testes.
    """
    
    logs: List[str] = field(default_factory=list)
    
    def atualizar_pontuacao(self, jogador_id: str, pontos_atuais: int, 
                           pontos_adicionados: int, motivo: str):
        """Loga mudança de pontuação"""
        if pontos_adicionados >= 0:
            mensagem = f"[{jogador_id}] +{pontos_adicionados} pts por '{motivo}' → Total: {pontos_atuais}"
        else:
            mensagem = f"[{jogador_id}] {pontos_adicionados} pts por '{motivo}' → Total: {pontos_atuais}"
        
        self.logs.append(mensagem)
        print(f"📊 {mensagem}")


@dataclass(eq=False)  # Comparação por identidade, não por valor
class HistoricoPontuacaoObserver(PontuacaoObserver):
    """
    Observer que mantém histórico completo de mudanças.
    
    GoF Observer Pattern: Concrete Observer
    Útil para exibir timeline de pontuação na UI.
    """
    
    historico: List[Dict] = field(default_factory=list)
    
    def atualizar_pontuacao(self, jogador_id: str, pontos_atuais: int, 
                           pontos_adicionados: int, motivo: str):
        """Registra mudança no histórico"""
        entrada = {
            "jogador_id": jogador_id,
            "pontos_atuais": pontos_atuais,
            "pontos_adicionados": pontos_adicionados,
            "motivo": motivo,
            "timestamp": len(self.historico)  # Índice como timestamp simplificado
        }
        self.historico.append(entrada)
    
    def obter_historico_jogador(self, jogador_id: str) -> List[Dict]:
        """Retorna histórico filtrado por jogador"""
        return [h for h in self.historico if h["jogador_id"] == jogador_id]

