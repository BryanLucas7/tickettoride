from app.core.domain.managers.gerenciador_baralho_vagoes import GerenciadorBaralhoVagoes
from app.core.domain.managers.gerenciador_baralho_bilhetes import GerenciadorBaralhoBilhetes
from app.core.domain.calculators.placar import Placar
from app.core.domain.managers.descarte_manager import DescarteManager
from app.core.domain.strategies.rota_dupla_validator import RotaDuplaValidator
from app.core.domain.calculators.verificador_bilhetes import VerificadorBilhetes
from app.constants import CARTAS_INICIAIS

try:
    from ....adapters.outbound.data.mapa_brasil import carregar_tabuleiro_brasil
except ImportError:  # Suporte para execuções fora do pacote "app"
    from app.adapters.outbound.data.mapa_brasil import carregar_tabuleiro_brasil


class JogoInicializador:
    """Responsável pela inicialização do jogo e configuração inicial."""

    def __init__(self, jogo):
        self.jogo = jogo

    def iniciar(self):
        """Inicializa o jogo

        Aplica princípios GRASP:
        - Controller: Jogo coordena a inicialização
        - Information Expert: Cada gerenciador possui suas cartas (SRP)
        """
        self._configurar_tabuleiro_padrao()

        # Inicializa componentes - SRP: gerenciadores separados para vagões e bilhetes
        self.jogo.estado.placar = Placar(jogadores=self.jogo.gerenciadorDeTurnos.jogadores)
        self.jogo.gerenciadorDeBaralhoVagoes = GerenciadorBaralhoVagoes()
        self.jogo.gerenciadorDeBaralhoBilhetes = GerenciadorBaralhoBilhetes()
        self.jogo.descarteManager = DescarteManager(
            pilha_descarte=self.jogo.gerenciadorDeBaralhoVagoes.descarteVagoes
        )
        self.jogo.estado.gerenciador_fim.resetar()
        self.jogo.estado.gerenciador_fim.total_jogadores = len(self.jogo.gerenciadorDeTurnos.jogadores)
        self.jogo.pathfinder = VerificadorBilhetes()  # Inicializa verificador de bilhetes

        # Distribui 4 cartas iniciais para cada jogador (regra oficial)
        self._distribuirCartasIniciais()

        # Distribui 3 bilhetes de destino para escolha inicial
        self._distribuirBilhetesIniciais()

        if self.jogo.tabuleiro.validador_duplas:
            self.jogo.tabuleiro.validador_duplas.numero_jogadores = len(self.jogo.gerenciadorDeTurnos.jogadores)

        self.jogo.estado.iniciado = True

    def _configurar_tabuleiro_padrao(self):
        """Popula o tabuleiro com o mapa brasileiro padrão."""

        info = carregar_tabuleiro_brasil(self.jogo.tabuleiro)
        rotas_duplas = info.get("rotas_duplas", []) if isinstance(info, dict) else []
        self.jogo.rotasDuplas = list(rotas_duplas)

        if rotas_duplas:
            validador = RotaDuplaValidator(
                numero_jogadores=len(self.jogo.gerenciadorDeTurnos.jogadores)
            )
            for rota_id_a, rota_id_b in rotas_duplas:
                rota_a = self.jogo.tabuleiro.obterRotaPorId(rota_id_a)
                rota_b = self.jogo.tabuleiro.obterRotaPorId(rota_id_b)
                if rota_a and rota_b:
                    validador.registrar_rota_dupla(rota_a, rota_b)
            self.jogo.tabuleiro.validador_duplas = validador

    def _distribuirCartasIniciais(self):
        """Distribui cartas de vagão iniciais para cada jogador

        Regra oficial: Cada jogador começa com CARTAS_INICIAIS cartas de vagão
        """
        for jogador in self.jogo.gerenciadorDeTurnos.jogadores:
            for _ in range(CARTAS_INICIAIS):
                carta = self.jogo.gerenciadorDeBaralhoVagoes.comprarCartaVagaoViewer(visivel=False)
                if carta:
                    jogador.comprarCartaVagao(carta)

        print(f"[OK] Distribuidas {CARTAS_INICIAIS} cartas iniciais para {len(self.jogo.gerenciadorDeTurnos.jogadores)} jogadores")

    def _distribuirBilhetesIniciais(self):
        """Distribui 3 bilhetes de destino para escolha inicial de cada jogador

        Regra oficial: Cada jogador recebe 3 bilhetes e DEVE ficar com pelo menos 2
        Os bilhetes recusados são devolvidos ao FINAL do baralho
        """
        for jogador in self.jogo.gerenciadorDeTurnos.jogadores:
            bilhetes = self.jogo.gerenciadorDeBaralhoBilhetes.comprar()
            # Armazena os bilhetes pendentes de escolha para este jogador
            self.jogo.estado.bilhetes_state.definir_pendentes_escolha(jogador.id, bilhetes)

        print(f" Distribuídos 3 bilhetes iniciais para {len(self.jogo.gerenciadorDeTurnos.jogadores)} jogadores (aguardando escolha)")