"""
Validador de existência de jogador.

SRP: Única responsabilidade - validar se jogador existe no jogo.
Reutilizável em qualquer contexto que precise validar jogador.

Extraído de CompraValidator para:
- Melhor separação de responsabilidades
- Reutilização em outros contexts (conquista de rota, bilhetes, etc)
- Facilitar testes unitários
"""

from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from ...entities.jogador import Jogador


@dataclass
class JogadorValidationResult:
    """
    Resultado da validação de jogador.
    
    Attributes:
        valido: Se o jogador foi encontrado
        erro: Mensagem de erro (se inválido)
        jogador: Instância do jogador (se válido)
    """
    valido: bool
    erro: Optional[str] = None
    jogador: Optional['Jogador'] = None
    
    @property
    def invalido(self) -> bool:
        """Conveniência para verificar se é inválido."""
        return not self.valido


class JogadorValidator:
    """
    Valida existência de jogador no jogo.
    
    SRP: Apenas verifica se jogador existe.
    Reutilizável em qualquer contexto que precise validar jogador.
    
    Exemplo de uso:
        validator = JogadorValidator(gerenciador_turnos)
        resultado = validator.validar("jogador-123")
        if resultado.invalido:
            raise HTTPException(status_code=404, detail=resultado.erro)
        jogador = resultado.jogador
    """
    
    def __init__(self, gerenciador_turnos):
        """
        Inicializa validator com gerenciador de turnos.
        
        Args:
            gerenciador_turnos: Gerenciador que contém lista de jogadores
        """
        self._gerenciador_turnos = gerenciador_turnos
    
    def validar(self, jogador_id: str) -> JogadorValidationResult:
        """
        Valida se jogador existe.
        
        Args:
            jogador_id: ID do jogador a ser validado
            
        Returns:
            JogadorValidationResult com jogador se válido, erro se inválido
        """
        if not jogador_id:
            return JogadorValidationResult(
                valido=False,
                erro="ID do jogador não fornecido"
            )
        
        jogador = self._gerenciador_turnos.obter_jogador_por_id(jogador_id)
        
        if not jogador:
            return JogadorValidationResult(
                valido=False,
                erro=f"Jogador {jogador_id} não encontrado"
            )
        
        return JogadorValidationResult(valido=True, jogador=jogador)
    
    def validar_jogador_atual(self, jogador_id: str) -> JogadorValidationResult:
        """
        Valida se jogador existe E é o jogador do turno atual.
        
        Args:
            jogador_id: ID do jogador a ser validado
            
        Returns:
            JogadorValidationResult
        """
        resultado = self.validar(jogador_id)
        if resultado.invalido:
            return resultado
        
        jogador_atual = self._gerenciador_turnos.jogadorAtual
        if jogador_atual and jogador_atual.id != jogador_id:
            return JogadorValidationResult(
                valido=False,
                erro=f"Não é o turno do jogador {jogador_id}. "
                     f"Turno atual: {jogador_atual.nome}"
            )
        
        return resultado
