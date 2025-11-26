"""
JogoBilhetesState - Gerenciador de estado de bilhetes pendentes.

Padrão GRASP: Information Expert
Princípio SRP: Responsável apenas por gerenciar bilhetes pendentes.

Extraído de Jogo para reduzir acoplamento e número de responsabilidades.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .bilhete_destino import BilheteDestino


@dataclass
class JogoBilhetesState:
    """
    Gerencia o estado de bilhetes pendentes do jogo.
    
    SRP: Responsável apenas por:
    - Bilhetes pendentes de escolha inicial
    - Bilhetes reservados para compra
    
    Extraído de Jogo para reduzir número de responsabilidades.
    """
    
    # Armazena os bilhetes pendentes de escolha inicial para cada jogador
    bilhetes_pendentes_escolha: Dict[str, List[BilheteDestino]] = field(default_factory=dict)
    # Armazena bilhetes sorteados aguardando confirmação de compra durante a partida
    bilhetes_pendentes_compra: Dict[str, List[BilheteDestino]] = field(default_factory=dict)
    
    # === Bilhetes Pendentes de Escolha (iniciais) ===
    
    def definir_pendentes_escolha(self, player_id: str, bilhetes: List[BilheteDestino]) -> None:
        """Define bilhetes pendentes de escolha inicial para um jogador."""
        self.bilhetes_pendentes_escolha[player_id] = bilhetes
    
    def obter_pendentes_escolha(self, player_id: str) -> Optional[List[BilheteDestino]]:
        """Obtém bilhetes pendentes de escolha inicial."""
        return self.bilhetes_pendentes_escolha.get(player_id)
    
    def tem_pendentes_escolha(self, player_id: str) -> bool:
        """Verifica se jogador tem bilhetes pendentes de escolha."""
        return player_id in self.bilhetes_pendentes_escolha
    
    def limpar_pendentes_escolha(self, player_id: str) -> None:
        """Remove bilhetes pendentes de escolha inicial."""
        self.bilhetes_pendentes_escolha.pop(player_id, None)
    
    def todos_jogadores_escolheram(self, jogadores_ids: List[str]) -> bool:
        """Verifica se todos os jogadores já fizeram suas escolhas iniciais."""
        return all(
            player_id not in self.bilhetes_pendentes_escolha 
            for player_id in jogadores_ids
        )
    
    # === Bilhetes Reservados (compra durante partida) ===
    
    def reservar_bilhetes(self, player_id: str, bilhetes: List[BilheteDestino]) -> None:
        """Reserva bilhetes para um jogador aguardando confirmação."""
        self.bilhetes_pendentes_compra[player_id] = bilhetes
    
    def obter_bilhetes_reservados(self, player_id: str) -> Optional[List[BilheteDestino]]:
        """Obtém os bilhetes reservados de um jogador."""
        return self.bilhetes_pendentes_compra.get(player_id)
    
    def limpar_bilhetes_reservados(self, player_id: str) -> None:
        """Remove os bilhetes reservados de um jogador."""
        self.bilhetes_pendentes_compra.pop(player_id, None)
    
    def tem_bilhetes_reservados(self, player_id: str) -> bool:
        """Verifica se jogador tem bilhetes reservados."""
        return player_id in self.bilhetes_pendentes_compra
