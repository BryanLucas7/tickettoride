import random
from dataclasses import dataclass, field
from typing import List

@dataclass
class Baralho:
    cartas: List = field(default_factory=list)

    def embaralhar(self):
        """Embaralha as cartas do baralho"""
        random.shuffle(self.cartas)

    def adicionar(self, carta, endOf: bool = True):
        """Adiciona uma carta ao baralho
        
        Args:
            carta: Carta a ser adicionada
            endOf: Se True, adiciona no final; se False, adiciona no início
        """
        if endOf:
            self.cartas.append(carta)
        else:
            self.cartas.insert(0, carta)
    
    def comprar(self):
        """Remove e retorna a última carta do baralho"""
        if self.cartas:
            return self.cartas.pop()
        return None
