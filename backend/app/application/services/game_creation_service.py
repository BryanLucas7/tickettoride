"""
Service para criação de jogos

GRASP Principles:
- Pure Fabrication: Serviço criado para extrair lógica de criação de jogo
- High Cohesion: Responsável apenas por criação e inicialização de jogos
- Low Coupling: Desacoplado dos routes, pode ser reutilizado
- Controller: Orquestra a criação do jogo e seus componentes
"""

from typing import List, Any, Set
import uuid
from fastapi import HTTPException

from ...core.domain.entities.jogo import Jogo
from ...core.domain.entities.jogador import Jogador
from ...core.domain.entities.cor import Cor
from ...adapters.inbound.http.schemas import CreateGameRequest


class GameCreationService:
    """
    Serviço responsável por criação de jogos.
    
    Extrai toda a lógica de criação de jogos do endpoint,
    tornando o código mais testável e reutilizável.
    """
    
    # Cores padrão disponíveis para jogadores
    CORES_PADRAO = [
        Cor.VERMELHO,
        Cor.AZUL,
        Cor.VERDE,
        Cor.AMARELO,
        Cor.PRETO
    ]
    
    def create_game(self, request: CreateGameRequest) -> Jogo:
        """
        Cria um novo jogo com base na requisição.
        
        Args:
            request: Dados da requisição contendo número de jogadores e opcionalmente
                    lista de jogadores com nome e cor
                    
        Returns:
            Jogo inicializado e pronto para ser usado
            
        Raises:
            HTTPException: Se houver erro na validação de cores ou jogadores
        """
        # Gera ID único para o jogo
        game_id = f"game-{uuid.uuid4()}"
        
        # Cria instância do jogo
        jogo = Jogo(id=game_id)
        
        # Adiciona jogadores ao jogo
        if request.jogadores:
            self._adicionar_jogadores_customizados(jogo, request.jogadores)
        else:
            self._adicionar_jogadores_padrao(jogo, request.numero_jogadores)
        
        # Inicializa o jogo (distribui cartas, bilhetes, etc.)
        jogo.iniciar()
        
        return jogo
    
    def _adicionar_jogadores_customizados(
        self, 
        jogo: Jogo, 
        jogadores_request: List[Any]
    ) -> None:
        """
        Adiciona jogadores customizados ao jogo.
        
        Args:
            jogo: Instância do jogo
            jogadores_request: Lista de payloads de jogadores com nome e cor
            
        Raises:
            HTTPException: Se cor for inválida ou duplicada
        """
        cores_usadas: Set[Cor] = set()
        
        for jogador_payload in jogadores_request:
            nome = jogador_payload.nome.strip()
            cor_payload = jogador_payload.cor.strip()
            
            # Valida e converte cor
            cor_enum = self._validar_cor(cor_payload)
            
            # Valida duplicação de cor
            if cor_enum in cores_usadas:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Cor duplicada: {cor_enum.value}"
                )
            cores_usadas.add(cor_enum)
            
            # Cria e adiciona jogador
            jogador = self._criar_jogador(nome, cor_enum)
            jogo.gerenciadorDeTurnos.adicionarJogador(jogador)
    
    def _adicionar_jogadores_padrao(
        self, 
        jogo: Jogo, 
        numero_jogadores: int
    ) -> None:
        """
        Adiciona jogadores com nomes e cores padrão.
        
        Args:
            jogo: Instância do jogo
            numero_jogadores: Número de jogadores a criar
        """
        # Limita ao número de cores disponíveis
        numero_jogadores = min(numero_jogadores, len(self.CORES_PADRAO))
        
        for i in range(numero_jogadores):
            nome = f"Jogador {i + 1}"
            cor = self.CORES_PADRAO[i]
            
            jogador = self._criar_jogador(nome, cor)
            jogo.gerenciadorDeTurnos.adicionarJogador(jogador)
    
    def _validar_cor(self, cor_str: str) -> Cor:
        """
        Valida e converte string de cor para enum Cor.
        
        Args:
            cor_str: String da cor (ex: "vermelho", "AZUL")
            
        Returns:
            Enum Cor correspondente
            
        Raises:
            HTTPException: Se cor for inválida
        """
        try:
            return Cor[cor_str.upper()]
        except KeyError:
            raise HTTPException(
                status_code=400, 
                detail=f"Cor inválida: {cor_str}"
            )
    
    def _criar_jogador(self, nome: str, cor: Cor) -> Jogador:
        """
        Cria uma instância de jogador com ID único.
        
        Args:
            nome: Nome do jogador
            cor: Cor do jogador
            
        Returns:
            Instância de Jogador
        """
        return Jogador(
            id=str(uuid.uuid4()),
            nome=nome,
            cor=cor
        )
