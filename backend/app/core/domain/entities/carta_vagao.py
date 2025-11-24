from dataclasses import dataclass
from .carta import Carta
from .cor import Cor

@dataclass
class CartaVagao(Carta):
    cor: Cor = Cor.VERMELHO
    ehLocomotiva: bool = False

    def __repr__(self):
        return f"<CartaVagao {self.cor.value} locomotiva={self.ehLocomotiva} id={self.id}>"
