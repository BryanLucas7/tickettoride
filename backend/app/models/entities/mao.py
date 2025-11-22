from dataclasses import dataclass, field
from typing import List
from .carta_vagao import CartaVagao

@dataclass
class Mao:
    cartasVagao: List[CartaVagao] = field(default_factory=list)

    def adicionarCarta(self, carta: CartaVagao):
        """Adiciona uma carta à mão"""
        self.cartasVagao.append(carta)

    def removerCartas(self, cartas: List[CartaVagao]) -> bool:
        """Remove as cartas especificadas da mão
        
        Returns:
            True se todas as cartas foram removidas com sucesso
        """
        for c in cartas:
            if c not in self.cartasVagao:
                return False
        for c in cartas:
            self.cartasVagao.remove(c)
        return True

    def getQuantidade(self, cor=None) -> int:
        """Retorna a quantidade de cartas na mão
        
        Args:
            cor: Se especificado, conta apenas cartas dessa cor
        """
        if cor is None:
            return len(self.cartasVagao)
        return sum(1 for c in self.cartasVagao if c.cor == cor and not c.ehLocomotiva)
