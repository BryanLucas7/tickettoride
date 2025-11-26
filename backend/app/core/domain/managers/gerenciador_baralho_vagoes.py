"""
Gerenciador de Baralho de Vagões.

Padrão GRASP: Information Expert - possui os dados das cartas de vagão
Padrão GRASP: Pure Fabrication - separa responsabilidade de gerenciamento de cartas
Princípio SRP: Gerencia APENAS cartas de vagão. Bilhetes são gerenciados
separadamente por GerenciadorBaralhoBilhetes.

Refatoração SRP: 
- CartaVagaoFactory: extraída para factories/carta_vagao_factory.py
- GerenciadorBaralhoVagoes: responsável pelo gerenciamento do baralho
- LocomotivaResetRule: regra de reset extraída (Strategy Pattern)
"""

from dataclasses import dataclass, field
from typing import List, Optional

from ..entities.baralho import Baralho
from ..entities.carta_vagao import CartaVagao
from ..rules import LocomotivaResetRule, CartasAbertasRule
from ..factories import CartaVagaoFactory


@dataclass
class GerenciadorBaralhoVagoes:
    """
    Gerenciador dedicado para cartas de vagão.
    
    Responsabilidades (SRP - apenas gerenciamento):
    - Gerenciar as 5 cartas abertas
    - Comprar cartas do baralho fechado ou abertas
    - Controlar pilha de descarte
    - Reabastecer baralho quando vazio
    
    NOTA: Criação de cartas delegada para CartaVagaoFactory (SRP).
    NOTA: Bilhetes de destino são gerenciados separadamente por
    GerenciadorBaralhoBilhetes (SRP).
    NOTA: Regra de reset por locomotivas delegada para LocomotivaResetRule (SRP/Strategy).
    """
    baralhoVagoes: Baralho = field(default_factory=Baralho)
    descarteVagoes: List[CartaVagao] = field(default_factory=list)
    cartasAbertas: List[CartaVagao] = field(default_factory=list)
    _reset_rule: Optional[CartasAbertasRule] = field(default=None, repr=False)

    def __post_init__(self):
        """Inicializa os baralhos após a criação."""
        # Strategy Pattern: usa regra padrão se não injetada
        if self._reset_rule is None:
            self._reset_rule = LocomotivaResetRule()
        
        self.inicializarBaralhoVagoes()
        self.inicializarCartasAbertas()

    def inicializarBaralhoVagoes(self):
        """Cria as 110 cartas de vagão do jogo usando Factory."""
        # Delega criação para CartaVagaoFactory (SRP)
        cartas, _ = CartaVagaoFactory.criar_baralho_completo()
        
        for carta in cartas:
            self.baralhoVagoes.adicionar(carta)

        # Embaralha o baralho após criar todas as cartas
        self.baralhoVagoes.embaralhar()

        print(f"[OK] Baralho de vagoes criado: {len(self.baralhoVagoes.cartas)} cartas")

    def inicializarCartasAbertas(self):
        """Inicializa as 5 cartas abertas visíveis na mesa

        Aplica Factory Method Pattern: CartaVagao já foi criada pelo Factory (inicializarBaralhoVagoes)
        Aplica GRASP Information Expert: GerenciadorDeBaralho gerencia as cartas abertas
        """
        for _ in range(5):
            carta = self.baralhoVagoes.comprar()
            if carta:
                self.cartasAbertas.append(carta)

        # Verifica se há 3+ locomotivas abertas (regra especial)
        self._verificarLocomotivas()

        print(f"[OK] Cartas abertas inicializadas: {len(self.cartasAbertas)} cartas visiveis")

    def _verificarLocomotivas(self):
        """Verifica regra especial: se 3+ locomotivas estão abertas, descarta todas e revela 5 novas

        Regra oficial: Se 3 ou mais locomotivas aparecerem nas 5 cartas abertas,
        todas são descartadas e 5 novas cartas são reveladas
        
        Refatoração SRP: Delega verificação para LocomotivaResetRule (Strategy Pattern).
        A regra pode ser substituída via injeção de dependência para testes.
        """
        # Strategy Pattern: delega decisão para regra injetada
        if not self._reset_rule.deve_resetar(self.cartasAbertas):
            return
        
        # Executa reset quando regra determina necessário
        locomotivas = sum(1 for carta in self.cartasAbertas if carta.ehLocomotiva)
        print(f"⚠️  {locomotivas} locomotivas abertas! Descartando todas e revelando 5 novas...")

        # Descarta todas as cartas abertas
        self.descarteVagoes.extend(self.cartasAbertas)
        self.cartasAbertas.clear()

        # Revela 5 novas cartas
        for _ in range(5):
            carta = self.baralhoVagoes.comprar()
            if carta:
                self.cartasAbertas.append(carta)

        # Verifica novamente (recursivo, caso apareçam 3+ locomotivas novamente)
        self._verificarLocomotivas()

    def comprarCartaVagaoViewer(self, visivel: bool = True) -> CartaVagao:
        """Compra uma carta vagão do baralho fechado

        Args:
            visivel: Parâmetro legado, ignorado

        Returns:
            Carta comprada do topo do baralho
        """
        _ = visivel  # Silenciar warning de parâmetro não utilizado
        carta = self.baralhoVagoes.comprar()
        if carta is None:
            self.reabastecerBaralhoVagaoVazio()
            carta = self.baralhoVagoes.comprar()
        return carta

    def comprarCartaVagaoVisivel(self, indice: int) -> CartaVagao:
        """Compra uma carta vagão visível pelo índice e repõe automaticamente

        Args:
            indice: Índice da carta nas 5 cartas abertas (0-4)

        Returns:
            Carta comprada ou None se índice inválido

        Aplica GRASP Information Expert: GerenciadorDeBaralho gerencia reposição automática
        """
        if indice < 0 or indice >= len(self.cartasAbertas):
            print(f"[ERRO] Indice invalido: {indice}")
            return None

        # Remove a carta escolhida das cartas abertas
        carta_escolhida = self.cartasAbertas.pop(indice)

        # Repõe com uma nova carta do baralho
        nova_carta = self.baralhoVagoes.comprar()
        if nova_carta is None:
            # Se baralho vazio, reabastece com descarte
            self.reabastecerBaralhoVagaoVazio()
            nova_carta = self.baralhoVagoes.comprar()

        if nova_carta:
            self.cartasAbertas.insert(indice, nova_carta)

            # Verifica se há 3+ locomotivas após reposição
            self._verificarLocomotivas()

        return carta_escolhida

    def obterCartasAbertas(self) -> List[CartaVagao]:
        """Retorna as 5 cartas abertas visíveis

        Returns:
            Lista com as 5 cartas abertas
        """
        return self.cartasAbertas[:]

    def reabastecerBaralhoVagaoVazio(self):
        """Reabastece o baralho de vagões com as cartas do descarte."""
        if not self.baralhoVagoes.cartas and self.descarteVagoes:
            self.baralhoVagoes.cartas = self.descarteVagoes[:]
            self.descarteVagoes.clear()
            self.baralhoVagoes.embaralhar()