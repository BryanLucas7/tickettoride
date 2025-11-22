from ..managers.gerenciador_de_turnos import GerenciadorDeTurnos
from ..managers.gerenciador_de_baralho import GerenciadorDeBaralho
from ..calculators.placar import Placar
from ..entities.tabuleiro import Tabuleiro
from ..managers.descarte_manager import DescarteManager
from ..strategies.validador_rotas_duplas import ValidadorRotasDuplas
from ..managers.gerenciador_fim_jogo import GerenciadorFimDeJogo
from ..calculators.verificador_bilhetes import VerificadorBilhetes

try:
    from ..data.mapa_brasil import carregar_tabuleiro_brasil
except ImportError:  # Suporte para execuções fora do pacote "app"
    from ...data.mapa_brasil import carregar_tabuleiro_brasil


class JogoInicializador:
    """Responsável pela inicialização do jogo e configuração inicial."""

    def __init__(self, jogo):
        self.jogo = jogo

    def iniciar(self):
        """Inicializa o jogo

        Aplica princípios GRASP:
        - Controller: Jogo coordena a inicialização
        - Information Expert: GerenciadorDeBaralho possui as cartas
        """
        self._configurar_tabuleiro_padrao()

        # Inicializa componentes
        self.jogo.placar = Placar(jogadores=self.jogo.gerenciadorDeTurnos.jogadores)
        self.jogo.gerenciadorDeBaralho = GerenciadorDeBaralho()
        self.jogo.descarteManager = DescarteManager(
            pilha_descarte=self.jogo.gerenciadorDeBaralho.descarteVagoes
        )
        self.jogo.gerenciadorFimDeJogo.resetar()
        self.jogo.gerenciadorFimDeJogo.total_jogadores = len(self.jogo.gerenciadorDeTurnos.jogadores)
        self.jogo.pathfinder = VerificadorBilhetes()  # Inicializa verificador de bilhetes

        # Distribui 4 cartas iniciais para cada jogador (regra oficial)
        self._distribuirCartasIniciais()

        # Distribui 3 bilhetes de destino para escolha inicial
        self._distribuirBilhetesIniciais()

        if self.jogo.tabuleiro.validador_duplas:
            self.jogo.tabuleiro.validador_duplas.numero_jogadores = len(self.jogo.gerenciadorDeTurnos.jogadores)

        self.jogo.iniciado = True

    def _configurar_tabuleiro_padrao(self):
        """Popula o tabuleiro com o mapa brasileiro padrão."""

        info = carregar_tabuleiro_brasil(self.jogo.tabuleiro)
        rotas_duplas = info.get("rotas_duplas", []) if isinstance(info, dict) else []
        self.jogo.rotasDuplas = list(rotas_duplas)

        if rotas_duplas:
            validador = ValidadorRotasDuplas(
                numero_jogadores=len(self.jogo.gerenciadorDeTurnos.jogadores)
            )
            for rota_id_a, rota_id_b in rotas_duplas:
                rota_a = self.jogo.tabuleiro.obterRotaPorId(rota_id_a)
                rota_b = self.jogo.tabuleiro.obterRotaPorId(rota_id_b)
                if rota_a and rota_b:
                    validador.registrar_rota_dupla(rota_a, rota_b)
            self.jogo.tabuleiro.validador_duplas = validador

    def _distribuirCartasIniciais(self):
        """Distribui 4 cartas de vagão para cada jogador

        Regra oficial: Cada jogador começa com 4 cartas de vagão
        """
        for jogador in self.jogo.gerenciadorDeTurnos.jogadores:
            for _ in range(4):
                carta = self.jogo.gerenciadorDeBaralho.comprarCartaVagaoViewer(visivel=False)
                if carta:
                    jogador.comprarCartaVagao(carta)

        print(f"[OK] Distribuidas 4 cartas iniciais para {len(self.jogo.gerenciadorDeTurnos.jogadores)} jogadores")

    def _distribuirBilhetesIniciais(self):
        """Distribui 3 bilhetes de destino para escolha inicial de cada jogador

        Regra oficial: Cada jogador recebe 3 bilhetes e DEVE ficar com pelo menos 2
        Os bilhetes recusados são devolvidos ao FINAL do baralho
        """
        for jogador in self.jogo.gerenciadorDeTurnos.jogadores:
            bilhetes = self.jogo.gerenciadorDeBaralho.comprarBilhetes()
            # Armazena os bilhetes pendentes de escolha para este jogador
            self.jogo.bilhetesPendentesEscolha[jogador.id] = bilhetes

        print(f" Distribuídos 3 bilhetes iniciais para {len(self.jogo.gerenciadorDeTurnos.jogadores)} jogadores (aguardando escolha)")