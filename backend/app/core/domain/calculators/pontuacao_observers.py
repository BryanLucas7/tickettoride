"""
Implementações concretas de PontuacaoObserver.

GoF Pattern: Observer (Concrete Observers)

Refatoração SRP: Observers concretos extraídos de placar.py para
separar implementações específicas da classe Placar principal.

Classes:
- LogPontuacaoObserver: Loga mudanças no console (debug/testes)
- HistoricoPontuacaoObserver: Mantém histórico completo (timeline UI)
"""

from dataclasses import dataclass, field
from typing import List, Dict

from .pontuacao_observer import PontuacaoObserver


@dataclass(eq=False)  # Comparação por identidade, não por valor
class LogPontuacaoObserver(PontuacaoObserver):
    """
    Observer que loga mudanças de pontuação no console.
    
    GoF Observer Pattern: Concrete Observer
    
    Útil para:
    - Debug durante desenvolvimento
    - Testes automatizados
    - Auditoria simples de pontuação
    
    Attributes:
        logs: Lista de mensagens de log registradas
    """
    
    logs: List[str] = field(default_factory=list)
    
    def atualizar_pontuacao(
        self, 
        jogador_id: str, 
        pontos_atuais: int, 
        pontos_adicionados: int, 
        motivo: str
    ) -> None:
        """
        Loga mudança de pontuação no console e na lista interna.
        
        Args:
            jogador_id: ID do jogador
            pontos_atuais: Pontuação total atual
            pontos_adicionados: Pontos adicionados (ou subtraídos se negativo)
            motivo: Descrição da mudança
        """
        if pontos_adicionados >= 0:
            mensagem = (
                f"[{jogador_id}] +{pontos_adicionados} pts por "
                f"'{motivo}' → Total: {pontos_atuais}"
            )
        else:
            mensagem = (
                f"[{jogador_id}] {pontos_adicionados} pts por "
                f"'{motivo}' → Total: {pontos_atuais}"
            )
        
        self.logs.append(mensagem)
        print(f"📊 {mensagem}")
    
    def limpar_logs(self) -> None:
        """Limpa todos os logs registrados."""
        self.logs.clear()
    
    def obter_logs(self) -> List[str]:
        """Retorna cópia dos logs."""
        return self.logs.copy()


@dataclass(eq=False)  # Comparação por identidade, não por valor
class HistoricoPontuacaoObserver(PontuacaoObserver):
    """
    Observer que mantém histórico completo de mudanças de pontuação.
    
    GoF Observer Pattern: Concrete Observer
    
    Útil para:
    - Exibir timeline de pontuação na UI
    - Replay de partidas
    - Análise estatística
    
    Attributes:
        historico: Lista de entradas com detalhes de cada mudança
    """
    
    historico: List[Dict] = field(default_factory=list)
    
    def atualizar_pontuacao(
        self, 
        jogador_id: str, 
        pontos_atuais: int, 
        pontos_adicionados: int, 
        motivo: str
    ) -> None:
        """
        Registra mudança no histórico.
        
        Args:
            jogador_id: ID do jogador
            pontos_atuais: Pontuação total atual
            pontos_adicionados: Pontos adicionados
            motivo: Descrição da mudança
        """
        entrada = {
            "jogador_id": jogador_id,
            "pontos_atuais": pontos_atuais,
            "pontos_adicionados": pontos_adicionados,
            "motivo": motivo,
            "timestamp": len(self.historico)  # Índice como timestamp simplificado
        }
        self.historico.append(entrada)
    
    def obter_historico_jogador(self, jogador_id: str) -> List[Dict]:
        """
        Retorna histórico filtrado por jogador.
        
        Args:
            jogador_id: ID do jogador para filtrar
            
        Returns:
            Lista de entradas do histórico deste jogador
        """
        return [h for h in self.historico if h["jogador_id"] == jogador_id]
    
    def obter_historico_completo(self) -> List[Dict]:
        """Retorna cópia do histórico completo."""
        return self.historico.copy()
    
    def limpar_historico(self) -> None:
        """Limpa todo o histórico."""
        self.historico.clear()
    
    def obter_ultimo_evento(self) -> Dict:
        """
        Retorna o último evento registrado.
        
        Returns:
            Última entrada do histórico ou dict vazio se não houver
        """
        return self.historico[-1] if self.historico else {}
