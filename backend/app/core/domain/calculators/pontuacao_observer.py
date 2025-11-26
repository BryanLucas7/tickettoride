"""
Interface Observer para mudanças de pontuação.

GoF Pattern: Observer
- Define interface para observers que recebem notificações de pontuação

GRASP: Protected Variations
- Interface abstrata protege implementações concretas de mudanças

Refatoração SRP: Interface extraída de placar.py para separar
contrato abstrato de implementação concreta.
"""

from abc import ABC, abstractmethod


class PontuacaoObserver(ABC):
    """
    Interface Observer para notificações de mudança de pontuação.
    
    GoF Observer Pattern: Interface Observer
    
    Implementações concretas podem:
    - Logar mudanças (LogPontuacaoObserver)
    - Manter histórico (HistoricoPontuacaoObserver)
    - Atualizar UI (FutureUIObserver)
    - Enviar webhooks, etc.
    """
    
    @abstractmethod
    def atualizar_pontuacao(
        self, 
        jogador_id: str, 
        pontos_atuais: int, 
        pontos_adicionados: int, 
        motivo: str
    ) -> None:
        """
        Notificação de mudança de pontuação.
        
        Chamado pelo Placar (Subject) quando pontos são adicionados/removidos.
        
        Args:
            jogador_id: ID do jogador que teve pontos alterados
            pontos_atuais: Pontuação total atual após a mudança
            pontos_adicionados: Quantidade de pontos adicionados 
                               (negativo se subtraídos)
            motivo: Descrição da razão da mudança 
                   (ex: "Rota Los Angeles - Seattle", "Bilhete completado")
        """
        pass
