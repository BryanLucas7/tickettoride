"""

Sistema de descarte de cartas ao conquistar rotas.

GRASP Principles Applied:
- Information Expert: DescarteManager conhece a pilha de descarte
- Controller: Gerencia o fluxo de descarte de cartas
- Low Coupling: Separado do Jogador e do Jogo

Design Decisions:
- Pilha de descarte separada do baralho principal
- Cartas descartadas podem ser reembaralhadas quando baralho acabar
"""

from dataclasses import dataclass, field
from typing import List
from app.core.domain.entities.carta_vagao import CartaVagao


@dataclass
class DescarteManager:
    """
    Gerencia a pilha de descarte de cartas.
    
    GRASP Information Expert: Conhece e gerencia cartas descartadas
    """
    
    pilha_descarte: List[CartaVagao] = field(default_factory=list)
    
    def descartar_cartas(self, cartas: List[CartaVagao]) -> int:
        """Adiciona cartas à pilha de descarte
        
        Args:
            cartas: Lista de CartaVagao a serem descartadas
            
        Returns:
            Quantidade de cartas descartadas
            
        GRASP Information Expert: Gerencia a pilha de descarte
        """
        if not cartas:
            return 0
        
        self.pilha_descarte.extend(cartas)
        return len(cartas)
    
    def obter_cartas_descartadas(self) -> List[CartaVagao]:
        """Retorna todas as cartas descartadas e limpa a pilha
        
        Usado para reembaralhar quando baralho principal acabar
        
        Returns:
            Lista com todas as cartas descartadas
        """
        cartas = self.pilha_descarte[:]
        self.pilha_descarte = []
        return cartas
    
    def quantidade_descartada(self) -> int:
        """Retorna quantidade de cartas na pilha de descarte"""
        return len(self.pilha_descarte)
    
    def limpar_descarte(self):
        """Limpa a pilha de descarte (usado para reset de jogo)"""
        self.pilha_descarte = []
