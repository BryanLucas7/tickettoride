from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from ..managers.gerenciador_de_turnos import GerenciadorDeTurnos
from ..managers.gerenciador_de_baralho import GerenciadorDeBaralho
from ..calculators.placar import Placar
from ..entities.tabuleiro import Tabuleiro
from ..entities.bilhete_destino import BilheteDestino
from ..managers.estado_compra_cartas import EstadoCompraCartas
from ..managers.descarte_manager import DescarteManager
from ..strategies.validador_rotas_duplas import ValidadorRotasDuplas
from ..managers.gerenciador_fim_jogo import GerenciadorFimDeJogo
from ..calculators.verificador_bilhetes import VerificadorBilhetes
from .jogo_inicializador import JogoInicializador
from .jogo_bilhetes_service import JogoBilhetesService
from .jogo_compras_service import JogoComprasService
from .jogo_actions_service import JogoActionsService

try:
    from ..data.mapa_brasil import carregar_tabuleiro_brasil
except ImportError:  # Suporte para execuções fora do pacote "app"
    from ...data.mapa_brasil import carregar_tabuleiro_brasil

@dataclass
class Jogo:
    id: int
    gerenciadorDeTurnos: GerenciadorDeTurnos = field(default_factory=GerenciadorDeTurnos)
    gerenciadorDeBaralho: Optional[GerenciadorDeBaralho] = None
    placar: Optional[Placar] = None
    tabuleiro: Tabuleiro = field(default_factory=Tabuleiro) #esta classe é necessaria visto ter o mapaBrasil.ts?d
    iniciado: bool = False
    finalizado: bool = False
    rotasDuplas: List[Tuple[str, str]] = field(default_factory=list)
    descarteManager: Optional[DescarteManager] = None
    gerenciadorFimDeJogo: GerenciadorFimDeJogo = field(default_factory=GerenciadorFimDeJogo)
    pathfinder: Optional[VerificadorBilhetes] = None  # Verificador de bilhetes completados
    # Armazena os bilhetes pendentes de escolha inicial para cada jogador
    bilhetesPendentesEscolha: Dict[str, List[BilheteDestino]] = field(default_factory=dict)
    # Armazena bilhetes sorteados aguardando confirmação de compra durante a partida
    bilhetesPendentesCompra: Dict[str, List[BilheteDestino]] = field(default_factory=dict)
    # Estado de compra de cartas do turno atual
    estadoCompraCartas: EstadoCompraCartas = field(default_factory=EstadoCompraCartas)
    # Services para responsabilidades separadas
    inicializador: JogoInicializador = field(init=False)
    bilhetesService: JogoBilhetesService = field(init=False)
    comprasService: JogoComprasService = field(init=False)
    actionsService: JogoActionsService = field(init=False)

    def __post_init__(self):
        self.inicializador = JogoInicializador(self)
        self.bilhetesService = JogoBilhetesService(self)
        self.comprasService = JogoComprasService(self)
        self.actionsService = JogoActionsService(self)

    def buscarJogador(self, jogador_id: str):
        """Retorna o jogador com o ID informado ou None."""
        return next(
            (j for j in self.gerenciadorDeTurnos.jogadores if str(j.id) == str(jogador_id)),
            None,
        )

    def iniciar(self):
        """Inicializa o jogo"""
        self.inicializador.iniciar()


    def escolherBilhetesIniciais(self, jogador_id: str, bilhetes_escolhidos_ids: List[object]) -> bool:
        """Processa a escolha de bilhetes iniciais de um jogador"""
        return self.bilhetesService.escolherBilhetesIniciais(jogador_id, bilhetes_escolhidos_ids)

    def comprarCartaDoBaralhoFechado(self, jogador_id: int) -> dict:
        """Compra uma carta do baralho fechado"""
        return self.comprasService.comprarCartaDoBaralhoFechado(jogador_id)

    def comprarCartaAberta(self, jogador_id: int, indice: int) -> dict:
        """Compra uma carta das 5 cartas abertas"""
        return self.comprasService.comprarCartaAberta(jogador_id, indice)

    def obterEstadoCompra(self) -> dict:
        """Retorna o estado atual de compra de cartas"""
        return self.comprasService.obterEstadoCompra()

    def proximar(self):
        """Avança para o próximo turno
        
        Reseta o estado de compra para o novo turno
        """
        # Reseta estado de compra de cartas
        self.estadoCompraCartas.resetar()
        
        return self.gerenciadorDeTurnos.proximoJogador()

    def jogar(self, acao: str, parametros: dict = None):
        """Executa uma ação de jogo"""
        self.actionsService.jogar(acao, parametros)

    def validarFimDeJogo(self) -> bool:
        """Valida se o jogo chegou ao fim"""
        return self.actionsService.validarFimDeJogo()

    def encerrar(self):
        """Encerra o jogo"""
        self.actionsService.encerrar()
