"""
EstadoJogo - Agrupa atributos de estado do jogo.

Refatoração SRP:
- Reduz número de atributos na classe Jogo
- Agrupa atributos relacionados ao estado do jogo
- Facilita serialização e clonagem de estado

GRASP Principles:
- Information Expert: EstadoJogo conhece e gerencia seu próprio estado
- Low Coupling: Isola estado do resto da lógica do jogo
"""

from dataclasses import dataclass, field
from typing import Optional

from ..managers.estado_compra_cartas import EstadoCompraCartas
from ..managers.gerenciador_fim_jogo import GerenciadorFimDeJogo
from ..calculators.placar import Placar
from .jogo_bilhetes_state import JogoBilhetesState


@dataclass
class EstadoJogo:
    """
    Agrupa atributos de estado do jogo.
    
    Responsabilidades:
    - Gerenciar estado de pontuação (placar)
    - Gerenciar estado de compra de cartas do turno
    - Gerenciar estado de bilhetes pendentes
    - Gerenciar estado de fim de jogo
    
    Benefícios:
    - Reduz atributos na classe Jogo de 15+ para ~10
    - Facilita testes (pode mockar estado completo)
    - Facilita serialização do estado
    """
    
    # Pontuação dos jogadores
    placar: Optional[Placar] = None
    
    # Estado de compra de cartas do turno atual
    estado_compra: EstadoCompraCartas = field(default_factory=EstadoCompraCartas)
    
    # Estado de bilhetes pendentes de escolha/reserva
    bilhetes_state: JogoBilhetesState = field(default_factory=JogoBilhetesState)
    
    # Gerenciador de condições de fim de jogo
    gerenciador_fim: GerenciadorFimDeJogo = field(default_factory=GerenciadorFimDeJogo)
    
    # Flags de estado do jogo
    iniciado: bool = False
    finalizado: bool = False
    
    def resetar_turno(self) -> None:
        """
        Reseta estado para novo turno.
        
        Chamado quando turno muda de jogador.
        """
        self.estado_compra.resetar()
    
    def iniciar(self) -> None:
        """Marca jogo como iniciado."""
        self.iniciado = True
    
    def finalizar(self) -> None:
        """Marca jogo como finalizado."""
        self.finalizado = True
    
    def atualizar_placar(self) -> None:
        """Atualiza pontuações no placar."""
        if self.placar:
            self.placar.atualizarPlacar()
