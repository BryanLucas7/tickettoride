"""
TASK #82: API - Endpoints completos de ações de jogo

Implementa Template Method Pattern para ações de turno.

GoF Patterns:
1. Template Method Pattern - AcaoTurno define template de execução

GRASP Principles:
- Controller: Ações coordenam operações do turno
- Indirection: Camada de API separa UI da lógica de negócio
- Information Expert: Cada ação conhece suas regras específicas
"""

from abc import ABC, abstractmethod
from typing import Optional

from .acao_turno_types import ResultadoAcao


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