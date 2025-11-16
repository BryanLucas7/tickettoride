"""
TASK #82: API - Endpoints completos de ações de jogo

Implementa Template Method Pattern para ações de turno e Singleton Pattern para GameManager.

GoF Patterns:
1. Template Method Pattern - AcaoTurno define template de execução
2. Singleton Pattern - GameManager tem única instância

GRASP Principles:
- Controller: Ações coordenam operações do turno
- Indirection: Camada de API separa UI da lógica de negócio
- Information Expert: Cada ação conhece suas regras específicas
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from enum import Enum


class TipoAcao(Enum):
    """Tipos de ações possíveis no turno"""
    COMPRAR_CARTAS = "comprar_cartas"
    CONQUISTAR_ROTA = "conquistar_rota"
    COMPRAR_BILHETES = "comprar_bilhetes"
    PASSAR_TURNO = "passar_turno"


@dataclass
class ResultadoAcao:
    """Resultado da execução de uma ação"""
    sucesso: bool
    mensagem: str
    dados: Dict[str, Any] = field(default_factory=dict)
    erros: List[str] = field(default_factory=list)


class AcaoTurno(ABC):
    """
    Template Method Pattern: Define template para execução de ações de turno.
    
    GoF Template Method Pattern:
    - Define esqueleto do algoritmo (executar)
    - Subclasses implementam passos específicos (validar_acao_especifica, executar_acao_especifica)
    
    GRASP Controller: Coordena execução de ação do turno
    """
    
    def __init__(self, jogo: 'Jogo', jogador_id: str):
        self.jogo = jogo
        self.jogador_id = jogador_id
        self.jogador = None
    
    def executar(self) -> ResultadoAcao:
        """
        Template Method: Define sequência de passos para executar ação.
        
        Sequência:
        1. validar() - Validações gerais
        2. validar_acao_especifica() - Validações específicas da ação
        3. executar_acao_especifica() - Executa ação concreta
        4. atualizar_estado() - Atualiza estado do jogo
        5. proximo_turno() - Avança para próximo jogador
        
        GoF Template Method Pattern: Método template
        """
        
        # Passo 1: Validações gerais (comum a todas ações)
        resultado_validacao = self._validar()
        if not resultado_validacao.sucesso:
            return resultado_validacao
        
        # Passo 2: Validações específicas da ação (hook method)
        resultado_validacao_especifica = self.validar_acao_especifica()
        if not resultado_validacao_especifica.sucesso:
            return resultado_validacao_especifica
        
        # Passo 3: Executa ação específica (abstract method)
        resultado_execucao = self.executar_acao_especifica()
        if not resultado_execucao.sucesso:
            return resultado_execucao
        
        # Passo 4: Atualiza estado do jogo (hook method)
        self.atualizar_estado(resultado_execucao)
        
        # Passo 5: Avança para próximo turno (hook method)
        self.proximo_turno()
        
        return resultado_execucao
    
    def _validar(self) -> ResultadoAcao:
        """Validações gerais comuns a todas ações"""
        
        # Verifica se jogo existe
        if not self.jogo:
            return ResultadoAcao(
                sucesso=False,
                mensagem="Jogo não encontrado",
                erros=["JOGO_NAO_ENCONTRADO"]
            )
        
        # Verifica se é turno deste jogador
        if self.jogo.jogador_atual_id != self.jogador_id:
            return ResultadoAcao(
                sucesso=False,
                mensagem=f"Não é seu turno. Turno atual: {self.jogo.jogador_atual_id}",
                erros=["NAO_E_SEU_TURNO"]
            )
        
        # Encontra jogador
        self.jogador = self.jogo.obter_jogador(self.jogador_id)
        if not self.jogador:
            return ResultadoAcao(
                sucesso=False,
                mensagem="Jogador não encontrado",
                erros=["JOGADOR_NAO_ENCONTRADO"]
            )
        
        return ResultadoAcao(sucesso=True, mensagem="Validação geral OK")
    
    @abstractmethod
    def validar_acao_especifica(self) -> ResultadoAcao:
        """
        Hook Method: Validações específicas de cada tipo de ação.
        
        Subclasses implementam validações específicas.
        """
        pass
    
    @abstractmethod
    def executar_acao_especifica(self) -> ResultadoAcao:
        """
        Abstract Method: Executa ação concreta.
        
        Subclasses DEVEM implementar a lógica específica da ação.
        """
        pass
    
    def atualizar_estado(self, resultado: ResultadoAcao):
        """
        Hook Method: Atualiza estado do jogo após ação.
        
        Implementação padrão vazia. Subclasses podem sobrescrever.
        """
        pass
    
    def proximo_turno(self):
        """
        Hook Method: Avança para próximo jogador.
        
        Implementação padrão. Subclasses podem sobrescrever se necessário.
        """
        self.jogo.avancar_turno()


# ============== AÇÕES CONCRETAS ==============

class AcaoComprarCartas(AcaoTurno):
    """
    Ação concreta: Comprar cartas do baralho.
    
    GoF Template Method Pattern: Concrete Class
    """
    
    def __init__(self, jogo: 'Jogo', jogador_id: str, cartas_selecionadas: List[str]):
        super().__init__(jogo, jogador_id)
        self.cartas_selecionadas = cartas_selecionadas
    
    def validar_acao_especifica(self) -> ResultadoAcao:
        """Valida se pode comprar cartas"""
        
        if len(self.cartas_selecionadas) > 2:
            return ResultadoAcao(
                sucesso=False,
                mensagem="Pode comprar no máximo 2 cartas por turno",
                erros=["LIMITE_CARTAS_EXCEDIDO"]
            )
        
        return ResultadoAcao(sucesso=True, mensagem="Validação específica OK")
    
    def executar_acao_especifica(self) -> ResultadoAcao:
        """Executa compra de cartas"""
        
        cartas_compradas = []
        
        for carta_id in self.cartas_selecionadas:
            # Lógica de comprar carta (simplificada)
            carta = self.jogo.comprar_carta(carta_id)
            if carta:
                self.jogador.comprarCartaVagao(carta)
                cartas_compradas.append(carta.id)
        
        return ResultadoAcao(
            sucesso=True,
            mensagem=f"Compradas {len(cartas_compradas)} cartas",
            dados={"cartas_compradas": cartas_compradas}
        )


class AcaoConquistarRota(AcaoTurno):
    """
    Ação concreta: Conquistar rota no tabuleiro.
    
    GoF Template Method Pattern: Concrete Class
    """
    
    def __init__(self, jogo: 'Jogo', jogador_id: str, rota_id: str, cartas_usadas: List[str]):
        super().__init__(jogo, jogador_id)
        self.rota_id = rota_id
        self.cartas_usadas = cartas_usadas
    
    def validar_acao_especifica(self) -> ResultadoAcao:
        """Valida se pode conquistar rota"""
        
        rota = self.jogo.obter_rota(self.rota_id)
        if not rota:
            return ResultadoAcao(
                sucesso=False,
                mensagem="Rota não encontrada",
                erros=["ROTA_NAO_ENCONTRADA"]
            )
        
        if rota.proprietario:
            return ResultadoAcao(
                sucesso=False,
                mensagem="Rota já conquistada",
                erros=["ROTA_JA_CONQUISTADA"]
            )
        
        return ResultadoAcao(sucesso=True, mensagem="Validação específica OK")
    
    def executar_acao_especifica(self) -> ResultadoAcao:
        """Executa conquista de rota"""
        
        rota = self.jogo.obter_rota(self.rota_id)
        
        # Conquista rota (integra com tasks anteriores)
        sucesso = rota.reivindicarRota(self.jogador, self.cartas_usadas)
        
        if sucesso:
            # Adiciona pontos (integra com Observer Pattern - Task #93)
            pontos = self.jogo.placar.adicionar_pontos_rota(
                self.jogador_id,
                rota.comprimento,
                f"{rota.cidadeA.nome}-{rota.cidadeB.nome}"
            )
            
            return ResultadoAcao(
                sucesso=True,
                mensagem=f"Rota conquistada! +{pontos} pontos",
                dados={
                    "rota_id": self.rota_id,
                    "pontos_ganhos": pontos
                }
            )
        else:
            return ResultadoAcao(
                sucesso=False,
                mensagem="Falha ao conquistar rota",
                erros=["FALHA_CONQUISTA"]
            )


class AcaoPassarTurno(AcaoTurno):
    """
    Ação concreta: Passar turno sem fazer nada.
    
    GoF Template Method Pattern: Concrete Class
    """
    
    def validar_acao_especifica(self) -> ResultadoAcao:
        """Passar turno não requer validações específicas"""
        return ResultadoAcao(sucesso=True, mensagem="Validação específica OK")
    
    def executar_acao_especifica(self) -> ResultadoAcao:
        """Executa passar turno"""
        return ResultadoAcao(
            sucesso=True,
            mensagem="Turno passado",
            dados={}
        )


# ============== SINGLETON: GAME MANAGER ==============

class GameManager:
    """
    Singleton Pattern: Gerencia única instância do jogo ativo.
    
    GoF Singleton Pattern:
    - __instance armazena única instância
    - __new__ garante criação de apenas uma instância
    - get_instance() retorna instância única
    
    GRASP Controller: Coordena criação e acesso ao jogo
    """
    
    _instance: Optional['GameManager'] = None
    _jogo: Optional['Jogo'] = None
    
    def __new__(cls):
        """
        Singleton Pattern: Garante única instância.
        
        Se instância não existe, cria nova.
        Se já existe, retorna existente.
        """
        if cls._instance is None:
            cls._instance = super(GameManager, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def get_instance(cls) -> 'GameManager':
        """
        Retorna instância única do GameManager.
        
        GoF Singleton Pattern: Método de acesso à instância
        """
        if cls._instance is None:
            cls._instance = GameManager()
        return cls._instance
    
    def criar_jogo(self, jogo: 'Jogo') -> bool:
        """Cria novo jogo (substitui jogo anterior se existir)"""
        self._jogo = jogo
        return True
    
    def obter_jogo(self) -> Optional['Jogo']:
        """Retorna jogo ativo"""
        return self._jogo
    
    def resetar(self):
        """Reseta GameManager (útil para testes)"""
        self._jogo = None
    
    @classmethod
    def resetar_singleton(cls):
        """Reseta singleton (útil para testes)"""
        cls._instance = None


# ============== MOCK DE JOGO (para testes) ==============

@dataclass
class JogoMock:
    """Mock simplificado de Jogo para demonstração"""
    
    jogador_atual_id: str = "jogador1"
    jogadores: Dict[str, Any] = field(default_factory=dict)
    rotas: Dict[str, Any] = field(default_factory=dict)
    placar: Any = None
    
    def obter_jogador(self, jogador_id: str):
        return self.jogadores.get(jogador_id)
    
    def obter_rota(self, rota_id: str):
        return self.rotas.get(rota_id)
    
    def comprar_carta(self, carta_id: str):
        """Mock de compra de carta"""
        return type('Carta', (), {'id': carta_id})()
    
    def avancar_turno(self):
        """Mock de avanço de turno"""
        pass
