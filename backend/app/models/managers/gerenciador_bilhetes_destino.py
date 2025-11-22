"""
Gerenciador de Bilhetes de Destino
===================================

Information Expert - Gerencia pilha de bilhetes de destino.

Responsabilidades:
- Manter pilha de bilhetes de destino
- Distribuir bilhetes para compra
- Receber bilhetes devolvidos
- Verificar quantidade disponível

GRASP Principles:
- Information Expert: Conhece pilha de bilhetes
- High Cohesion: Focado em gerenciar bilhetes de destino
"""

from dataclasses import dataclass, field
from typing import List
from .baralho import Baralho
from .bilhete_destino import BilheteDestino, BILHETES_DESTINO


@dataclass
class GerenciadorBilhetesDestino:
    pilha: Baralho = field(default_factory=Baralho)

    def __post_init__(self):
        """Inicializa pilha com todos os bilhetes"""
        if not self.pilha.cartas:
            self.pilha.cartas = BILHETES_DESTINO.copy()
            self.pilha.embaralhar()

    def comprar_bilhetes_para_escolha(self, quantidade: int = 3) -> List[BilheteDestino]:
        """
        Compra bilhetes do topo da pilha para o jogador escolher.

        Args:
            quantidade: Quantidade de bilhetes a comprar (padrão: 3)

        Returns:
            Lista de bilhetes disponíveis para escolha

        Nota: Se pilha tiver menos que a quantidade solicitada,
              retorna todos os disponíveis.
        """
        bilhetes_comprados = []

        # Comprar até a quantidade solicitada ou até acabar a pilha
        for _ in range(min(quantidade, len(self.pilha.cartas))):
            bilhete = self.pilha.comprar()
            if bilhete:
                bilhetes_comprados.append(bilhete)

        return bilhetes_comprados

    def devolver_bilhetes(self, bilhetes: List[BilheteDestino]):
        """
        Devolve bilhetes recusados ao final da pilha.

        Args:
            bilhetes: Lista de bilhetes a devolver
        """
        for bilhete in bilhetes:
            self.pilha.adicionar(bilhete, endOf=True)

    def quantidade_disponivel(self) -> int:
        """Retorna quantidade de bilhetes disponíveis na pilha"""
        return len(self.pilha.cartas)

    def resetar(self):
        """Reseta pilha com todos os bilhetes embaralhados"""
        self.pilha.cartas = BILHETES_DESTINO.copy()
        self.pilha.embaralhar()