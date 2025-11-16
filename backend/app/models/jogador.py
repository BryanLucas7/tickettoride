import uuid
from dataclasses import dataclass, field
from typing import List
from .cor import Cor
from .mao import Mao
from .bilhete_destino import BilheteDestino

@dataclass
class Jogador:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    nome: str = ""
    cor: Cor = None
    cartasVagao: List = field(default_factory=list)  # Collection de CartaVagao
    mao: Mao = field(default_factory=Mao)
    bilhetes: List[BilheteDestino] = field(default_factory=list)
    vagoes: List = field(default_factory=list)  # Lista de vagões disponíveis
    pontuacao: int = 0

    def __post_init__(self):
        # Inicializa com 45 vagões (padrão do jogo)
        if not self.vagoes:
            self.vagoes = list(range(45))

    def comprarCartaVagao(self, carta):
        """Compra uma carta vagão e adiciona à mão"""
        self.mao.adicionarCarta(carta)
        self.cartasVagao.append(carta)

    def removerCartasVagao(self, cartas: List):
        """Remove cartas tanto da mão quanto do inventário plano."""

        if not self.mao.removerCartas(cartas):
            return False

        for carta in cartas:
            if carta in self.cartasVagao:
                self.cartasVagao.remove(carta)

        return True

    def comprarBilhetesDestino(self, bilhetes: List[BilheteDestino]) -> List[BilheteDestino]:
        """Compra bilhetes de destino
        
        Returns:
            Lista de bilhetes aceitos pelo jogador
        """
        # Por simplicidade, aceita todos os bilhetes
        aceitos = bilhetes[:]
        self.bilhetes.extend(aceitos)
        return aceitos

    def reivindicarRota(self, rota):
        """Reivindica uma rota no tabuleiro"""
        # Remove vagões necessários
        if len(self.vagoes) >= rota.comprimento:
            for _ in range(rota.comprimento):
                self.vagoes.pop()
            return True
        return False

    def passarTurno(self):
        """Passa o turno sem realizar ação"""
        pass

    def receberCarta(self, carta):
        """Recebe uma carta (alternativa a comprarCartaVagao)"""
        self.comprarCartaVagao(carta)

    def revelarMaoParcial(self):
        """Revela parcialmente a mão para a UI"""
        return self.mao.cartasVagao

    def escolherCoresDisponiveis(self):
        """Retorna as cores disponíveis na mão do jogador"""
        from collections import Counter
        return Counter([c.cor for c in self.mao.cartasVagao if not c.ehLocomotiva])
