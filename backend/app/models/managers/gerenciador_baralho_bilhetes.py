from dataclasses import dataclass, field
from ..entities.baralho import Baralho
from ..entities.bilhete_destino import BilheteDestino, BILHETES_DESTINO
from typing import List

@dataclass
class GerenciadorBaralhoBilhetes:
    baralhoBilhetes: Baralho = field(default_factory=Baralho)

    def __post_init__(self):
        """Inicializa o baralho de bilhetes após a criação"""
        self.inicializarBaralhoBilhetes()

    def inicializarBaralhoBilhetes(self):
        """Cria o baralho com os 30 bilhetes de destino do jogo"""
        # Adiciona todos os bilhetes predefinidos
        for bilhete in BILHETES_DESTINO:
            self.baralhoBilhetes.adicionar(bilhete)

        # Embaralha o baralho de bilhetes
        self.baralhoBilhetes.embaralhar()

        print(f"[OK] Baralho de bilhetes criado: {len(self.baralhoBilhetes.cartas)} bilhetes")

    def comprarBilhetes(self) -> List[BilheteDestino]:
        """Compra bilhetes de destino do baralho"""
        bilhetes = []
        for _ in range(3):  # Normalmente são 3 bilhetes
            bilhete = self.baralhoBilhetes.comprar()
            if bilhete:
                bilhetes.append(bilhete)
        return bilhetes

    def devolverBilhetes(self, bilhetes: List[BilheteDestino]):
        """Devolve bilhetes não aceitos ao fundo do baralho"""
        for bilhete in bilhetes:
            self.baralhoBilhetes.adicionar(bilhete, endOf=True)  # Adiciona ao FINAL do baralho