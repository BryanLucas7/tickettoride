from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Union

from app.core.domain.managers.gerenciador_de_turnos import GerenciadorDeTurnos
from app.core.domain.managers.gerenciador_baralho_vagoes import GerenciadorBaralhoVagoes
from app.core.domain.managers.gerenciador_baralho_bilhetes import GerenciadorBaralhoBilhetes
from app.core.domain.calculators.placar import Placar
from .tabuleiro import Tabuleiro
from .bilhete_destino import BilheteDestino
from .rota import Rota
from .jogador import Jogador
from .jogo_bilhetes_state import JogoBilhetesState
from app.core.domain.managers.estado_compra_cartas import EstadoCompraCartas
from app.core.domain.managers.descarte_manager import DescarteManager
from app.core.domain.managers.gerenciador_fim_jogo import GerenciadorFimDeJogo
from app.core.domain.calculators.verificador_bilhetes import VerificadorBilhetes
from .jogo_inicializador import JogoInicializador
from .jogo_bilhetes_service import JogoBilhetesService
from .jogo_compras_service import JogoComprasService
from .jogo_actions_service import JogoActionsService
from .estado_jogo import EstadoJogo


@dataclass
class Jogo:
    """
    Entidade principal do jogo Ticket to Ride.
    
    Refatoração SRP: 
    - Estado de bilhetes extraído para JogoBilhetesState
    - Estado do jogo agrupado em EstadoJogo
    - Services expostos como propriedades públicas (evita thin wrappers)
    
    A classe Jogo atua como Facade, delegando para services especializados.
    
    Acesso a services (preferido):
        jogo.compras.comprarCartaDoBaralhoFechado(jogador_id)
        jogo.bilhetes.escolherBilhetesIniciais(jogador_id, ids)
        jogo.acoes.jogar("comprar_carta")
    
    Componentes:
    - gerenciadorDeTurnos: Gerencia turnos e jogadores
    - gerenciadorDeBaralhoVagoes: Gerencia baralho de cartas de vagão (SRP)
    - gerenciadorDeBaralhoBilhetes: Gerencia baralho de bilhetes de destino (SRP)
    - estado: Agrupa placar, estado_compra, bilhetes_state, etc (SRP)
    - tabuleiro: Gerencia rotas do mapa
    """
    id: int
    gerenciadorDeTurnos: GerenciadorDeTurnos = field(default_factory=GerenciadorDeTurnos)
    gerenciadorDeBaralhoVagoes: Optional[GerenciadorBaralhoVagoes] = None
    gerenciadorDeBaralhoBilhetes: Optional[GerenciadorBaralhoBilhetes] = None
    tabuleiro: Tabuleiro = field(default_factory=Tabuleiro)
    rotasDuplas: List[Tuple[str, str]] = field(default_factory=list)
    descarteManager: Optional[DescarteManager] = None
    pathfinder: Optional[VerificadorBilhetes] = None
    
    # Estado agrupado (reduz atributos - SRP)
    estado: EstadoJogo = field(default_factory=EstadoJogo)
    
    # Services expostos publicamente (evita thin wrappers)
    _inicializador: JogoInicializador = field(init=False, repr=False)
    _bilhetesService: JogoBilhetesService = field(init=False, repr=False)
    _comprasService: JogoComprasService = field(init=False, repr=False)
    _actionsService: JogoActionsService = field(init=False, repr=False)

    def __post_init__(self):
        self._ensure_internal_services()

    def _ensure_internal_services(self, force_refresh: bool = False) -> None:
        """
        Garante que os services internos existam e estejam consistentes.

        Útil após unpickle ou inicialização para reconstruir services que
        dependem de gerenciadores do jogo.
        """
        # Jogos antigos gravados em pickle podem não ter atributos introduzidos depois
        if not hasattr(self, "estado") or self.estado is None:
            self.estado = EstadoJogo()
        if not hasattr(self, "gerenciadorDeTurnos") or self.gerenciadorDeTurnos is None:
            self.gerenciadorDeTurnos = GerenciadorDeTurnos()
        if not hasattr(self, "gerenciadorDeBaralhoVagoes"):
            self.gerenciadorDeBaralhoVagoes = None
        if not hasattr(self, "gerenciadorDeBaralhoBilhetes"):
            self.gerenciadorDeBaralhoBilhetes = None
        if not hasattr(self, "descarteManager"):
            self.descarteManager = None

        if force_refresh or not hasattr(self, "_inicializador") or self._inicializador is None:
            self._inicializador = JogoInicializador(self)
        if force_refresh or not hasattr(self, "_bilhetesService") or self._bilhetesService is None:
            self._bilhetesService = JogoBilhetesService(self)
        if force_refresh or not hasattr(self, "_comprasService") or self._comprasService is None:
            self._comprasService = JogoComprasService(self)
        if force_refresh or not hasattr(self, "_actionsService") or self._actionsService is None:
            self._actionsService = JogoActionsService(self)

    # === Properties para expor services (evita thin wrappers) ===
    
    @property
    def compras(self) -> JogoComprasService:
        """
        Service para operações de compra de cartas.
        
        Uso: jogo.compras.comprarCartaDoBaralhoFechado(jogador_id)
        """
        self._ensure_internal_services()
        return self._comprasService
    
    @property
    def bilhetes(self) -> JogoBilhetesService:
        """
        Service para operações com bilhetes de destino.
        
        Uso: jogo.bilhetes.escolherBilhetesIniciais(jogador_id, ids)
        """
        self._ensure_internal_services()
        return self._bilhetesService
    
    @property
    def acoes(self) -> JogoActionsService:
        """
        Service para ações gerais do jogo.
        
        Uso: jogo.acoes.jogar("comprar_carta")
        """
        self._ensure_internal_services()
        return self._actionsService

    # === Métodos principais ===

    def buscarJogador(self, jogador_id: str):
        """
        Retorna o jogador com o ID informado ou None.
        
        GRASP Information Expert: Delega para GerenciadorDeTurnos.
        """
        return self.gerenciadorDeTurnos.obter_jogador_por_id(jogador_id)

    def iniciar(self):
        """Inicializa o jogo"""
        self._inicializador.iniciar()
        # Reconstrói services para garantir que validadores usem gerenciadores inicializados
        self._ensure_internal_services(force_refresh=True)

    def proximar(self):
        """Avança para o próximo turno
        
        Reseta o estado de compra para o novo turno
        """
        self.estado.resetar_turno()
        return self.gerenciadorDeTurnos.proximoJogador()

    def resetar_estado_compra(self) -> None:
        """Reseta o estado de compra de cartas do turno atual."""
        self.estado.resetar_turno()

    def passar_turno(self) -> str:
        """Passa para o próximo jogador."""
        return self.gerenciadorDeTurnos.proximoJogador()
    
    def obter_ou_criar_gerenciador_fim(self) -> GerenciadorFimDeJogo:
        """
        Obtém gerenciador de fim de jogo existente ou cria novo.
        
        Information Expert (GRASP): Jogo conhece seus próprios gerenciadores.
        """
        gerenciador = self.estado.gerenciador_fim
        if gerenciador is None:
            gerenciador = GerenciadorFimDeJogo(
                total_jogadores=len(self.gerenciadorDeTurnos.jogadores)
            )
            self.estado.gerenciador_fim = gerenciador
        else:
            gerenciador.total_jogadores = len(self.gerenciadorDeTurnos.jogadores)
        
        return gerenciador

    def rotas_do_jogador(self, jogador_or_id: Union[Jogador, str]) -> List[Rota]:
        """
        Obtém todas as rotas conquistadas por um jogador específico.
        
        GRASP Information Expert: Jogo conhece seu tabuleiro e suas rotas.
        """
        if isinstance(jogador_or_id, str):
            jogador = self.buscarJogador(jogador_or_id)
            if jogador is None:
                raise ValueError(f"Jogador com ID '{jogador_or_id}' não encontrado")
        else:
            jogador = jogador_or_id
        
        return [r for r in self.tabuleiro.rotas if r.proprietario == jogador]
