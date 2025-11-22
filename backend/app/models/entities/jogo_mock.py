"""
Mock simplificado de Jogo para demonstração e testes.
"""

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class JogoMock:
    """Mock simplificado de Jogo para demonstração"""

    jogador_atual_id: str = "jogador1"
    jogadores: Dict[str, Any] = field(default_factory=dict)
    rotas: Dict[str, Any] = field(default_factory=dict)
    placar: Any = None

    def obter_jogador(self, jogador_id: str):
        return self.jogadores.get(jogador_id)

    def obter_rota(self, rota_id: str):
        return self.rotas.get(rota_id)

    def comprar_carta(self, carta_id: str):
        """Mock de compra de carta"""
        return type('Carta', (), {'id': carta_id})()

    def avancar_turno(self):
        """Mock de avanço de turno"""
        pass