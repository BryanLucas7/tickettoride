"""
ConquestEvent - Evento emitido após conquista de rota.

GoF Pattern: Observer
- Contém dados do evento para observers processarem
"""

from dataclasses import dataclass

from ..entities.jogador import Jogador
from ..entities.rota import Rota


@dataclass
class ConquestEvent:
    """
    Evento emitido após conquista de rota.
    
    Contém todos os dados necessários para observers processarem
    a conquista (pontuação, verificação de fim, logging, etc).
    
    Attributes:
        jogador: Jogador que conquistou a rota
        rota: Rota que foi conquistada
        pontos_ganhos: Pontos obtidos pela conquista
        trens_restantes: Trens restantes do jogador após a conquista
    """
    jogador: Jogador
    rota: Rota
    pontos_ganhos: int
    trens_restantes: int
    
    @property
    def nome_rota(self) -> str:
        """Nome formatado da rota para logs/mensagens."""
        return f"{self.rota.cidadeA.nome} → {self.rota.cidadeB.nome}"
