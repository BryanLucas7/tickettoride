from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Union

from app.core.domain.managers.gerenciador_de_turnos import GerenciadorDeTurnos
from app.core.domain.managers.gerenciador_baralho_vagoes import GerenciadorBaralhoVagoes as GerenciadorDeBaralho
from app.core.domain.calculators.placar import Placar
from .tabuleiro import Tabuleiro
from .bilhete_destino import BilheteDestino
from .rota import Rota
from .jogador import Jogador
from app.core.domain.managers.estado_compra_cartas import EstadoCompraCartas
from app.core.domain.managers.descarte_manager import DescarteManager
from app.core.domain.managers.gerenciador_fim_jogo import GerenciadorFimDeJogo
from app.core.domain.calculators.verificador_bilhetes import VerificadorBilhetes
from .jogo_inicializador import JogoInicializador
from .jogo_bilhetes_service import JogoBilhetesService
from .jogo_compras_service import JogoComprasService
from .jogo_actions_service import JogoActionsService

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
        """
        Retorna o jogador com o ID informado ou None.
        
        GRASP Information Expert: Delega para GerenciadorDeTurnos.
        """
        return self.gerenciadorDeTurnos.obter_jogador_por_id(jogador_id)

    def iniciar(self):
        """Inicializa o jogo"""
        self.inicializador.iniciar()


    def escolherBilhetesIniciais(self, jogador_id: str, bilhetes_escolhidos_ids: List[object]) -> bool:
        """Processa a escolha de bilhetes iniciais de um jogador"""
        return self.bilhetesService.escolherBilhetesIniciais(jogador_id, bilhetes_escolhidos_ids)

    def comprarCartaDoBaralhoFechado(self, jogador_id: str) -> dict:
        """Compra uma carta do baralho fechado"""
        return self.comprasService.comprarCartaDoBaralhoFechado(jogador_id)

    def comprarCartaAberta(self, jogador_id: str, indice: int) -> dict:
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

    def resetar_estado_compra(self) -> None:
        """Reseta o estado de compra de cartas do turno atual.
        
        Encapsula o acesso direto ao estadoCompraCartas.
        Segue Information Expert: Jogo conhece seu próprio estado.
        """
        self.estadoCompraCartas.resetar()

    def passar_turno(self) -> str:
        """Passa para o próximo jogador.
        
        Returns:
            ID do próximo jogador
        """
        return self.gerenciadorDeTurnos.nextTurn()

    def reservar_bilhetes(self, player_id: str, bilhetes: List[BilheteDestino]) -> None:
        """Reserva bilhetes para um jogador aguardando confirmação.
        
        Args:
            player_id: ID do jogador
            bilhetes: Lista de bilhetes reservados
        """
        self.bilhetesPendentesCompra[player_id] = bilhetes

    def obter_bilhetes_reservados(self, player_id: str) -> Optional[List[BilheteDestino]]:
        """Obtém os bilhetes reservados de um jogador.
        
        Args:
            player_id: ID do jogador
            
        Returns:
            Lista de bilhetes reservados ou None se não houver
        """
        return self.bilhetesPendentesCompra.get(player_id)

    def limpar_bilhetes_reservados(self, player_id: str) -> None:
        """Remove os bilhetes reservados de um jogador.
        
        Args:
            player_id: ID do jogador
        """
        self.bilhetesPendentesCompra.pop(player_id, None)

    def jogar(self, acao: str, parametros: dict = None):
        """Executa uma ação de jogo"""
        self.actionsService.jogar(acao, parametros)

    def validarFimDeJogo(self) -> bool:
        """Valida se o jogo chegou ao fim"""
        return self.actionsService.validarFimDeJogo()

    def encerrar(self):
        """Encerra o jogo"""
        self.actionsService.encerrar()
    
    def obter_ou_criar_gerenciador_fim(self) -> GerenciadorFimDeJogo:
        """
        Obtém gerenciador de fim de jogo existente ou cria novo.
        
        Information Expert (GRASP): Jogo conhece seus próprios gerenciadores
        e é responsável por garantir que estejam configurados corretamente.
        
        Returns:
            GerenciadorFimDeJogo atualizado com total de jogadores correto
            
        Example:
            >>> gerenciador = jogo.obter_ou_criar_gerenciador_fim()
            >>> gerenciador.verificar_condicao_fim(trens_restantes=2)
        """
        if self.gerenciadorFimDeJogo is None:
            self.gerenciadorFimDeJogo = GerenciadorFimDeJogo(
                total_jogadores=len(self.gerenciadorDeTurnos.jogadores)
            )
        else:
            # Atualizar total de jogadores (pode ter mudado durante o jogo)
            self.gerenciadorFimDeJogo.total_jogadores = len(
                self.gerenciadorDeTurnos.jogadores
            )
        
        return self.gerenciadorFimDeJogo

    def rotas_do_jogador(self, jogador_or_id: Union[Jogador, str]) -> List[Rota]:
        """
        Obtém todas as rotas conquistadas por um jogador específico.
        
        GRASP Information Expert: Jogo conhece seu tabuleiro e suas rotas,
        sendo o responsável natural por fornecer essa informação.
        
        Args:
            jogador_or_id: Instância de Jogador ou ID do jogador (string)
            
        Returns:
            Lista de rotas conquistadas pelo jogador
            
        Raises:
            ValueError: Se o jogador não for encontrado (quando ID é fornecido)
            
        Examples:
            >>> # Usando instância de jogador
            >>> rotas = jogo.rotas_do_jogador(jogador)
            >>> len(rotas)
            3
            
            >>> # Usando ID do jogador
            >>> rotas = jogo.rotas_do_jogador("player-123")
            >>> all(r.proprietario.id == "player-123" for r in rotas)
            True
        """
        # Se receber um ID, buscar o jogador
        if isinstance(jogador_or_id, str):
            jogador = self.buscarJogador(jogador_or_id)
            if jogador is None:
                raise ValueError(f"Jogador com ID '{jogador_or_id}' não encontrado")
        else:
            jogador = jogador_or_id
        
        # Retornar rotas conquistadas pelo jogador
        return [r for r in self.tabuleiro.rotas if r.proprietario == jogador]
