from dataclasses import dataclass, field
from app.core.domain.entities.baralho import Baralho
from app.core.domain.entities.carta_vagao import CartaVagao
from app.core.domain.entities.bilhete_destino import BilheteDestino, BILHETES_DESTINO
from app.core.domain.entities.cor import Cor
from typing import List

@dataclass
class GerenciadorBaralhoVagoes:
    baralhoVagoes: Baralho = field(default_factory=Baralho)
    descarteVagoes: List[CartaVagao] = field(default_factory=list)
    cartasAbertas: List[CartaVagao] = field(default_factory=list)  # 5 cartas visíveis na mesa
    baralhoBilhetes: Baralho = field(default_factory=Baralho)  # Baralho de bilhetes de destino

    def __post_init__(self):
        """Inicializa os baralhos de vagões e bilhetes após a criação"""
        self.inicializarBaralhoVagoes()
        self.inicializarCartasAbertas()
        self.inicializarBaralhoBilhetes()

    def inicializarBaralhoVagoes(self):
        """Cria as 110 cartas de vagão do jogo"""
        contador_id = 1

        # Cores normais: 12 cartas de cada (8 cores x 12 = 96 cartas)
        cores = [
            Cor.ROXO,
            Cor.BRANCO,
            Cor.AZUL,
            Cor.AMARELO,
            Cor.LARANJA,
            Cor.PRETO,
            Cor.VERMELHO,
            Cor.VERDE
        ]

        for cor in cores:
            for _ in range(12):
                carta = CartaVagao(
                    id=contador_id,
                    cor=cor,
                    ehLocomotiva=False
                )
                self.baralhoVagoes.adicionar(carta)
                contador_id += 1

        # Locomotivas: 14 cartas coringa dedicadas
        for _ in range(14):
            carta = CartaVagao(
                id=contador_id,
                cor=Cor.LOCOMOTIVA,
                ehLocomotiva=True
            )
            self.baralhoVagoes.adicionar(carta)
            contador_id += 1

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
        """
        locomotivas = sum(1 for carta in self.cartasAbertas if carta.ehLocomotiva)

        if locomotivas >= 3:
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
        """Reabastece o baralho de vagões com as cartas do descarte"""
        if not self.baralhoVagoes.cartas and self.descarteVagoes:
            self.baralhoVagoes.cartas = self.descarteVagoes[:]
            self.descarteVagoes.clear()
            self.baralhoVagoes.embaralhar()

    # === MÉTODOS PARA BILHETES DE DESTINO ===

    def inicializarBaralhoBilhetes(self):
        """Cria o baralho com os 30 bilhetes de destino do jogo"""
        # Adiciona todos os bilhetes predefinidos
        for bilhete in BILHETES_DESTINO:
            self.baralhoBilhetes.adicionar(bilhete)

        # Embaralha o baralho de bilhetes
        self.baralhoBilhetes.embaralhar()

        print(f"[OK] Baralho de bilhetes criado: {len(self.baralhoBilhetes.cartas)} bilhetes")

    def comprarBilhetes(self) -> List[BilheteDestino]:
        """Compra bilhetes de destino do baralho
        
        Returns:
            Lista com 3 bilhetes de destino
        """
        bilhetes = []
        for _ in range(3):  # Normalmente são 3 bilhetes
            bilhete = self.baralhoBilhetes.comprar()
            if bilhete:
                bilhetes.append(bilhete)
        return bilhetes

    def devolverBilhetes(self, bilhetes: List[BilheteDestino]):
        """Devolve bilhetes não aceitos ao fundo do baralho
        
        Args:
            bilhetes: Lista de bilhetes a serem devolvidos
        """
        for bilhete in bilhetes:
            self.baralhoBilhetes.adicionar(bilhete, endOf=True)  # Adiciona ao FINAL do baralho