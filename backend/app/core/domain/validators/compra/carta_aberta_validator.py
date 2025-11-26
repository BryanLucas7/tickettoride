"""
Validador de compra de carta aberta (das 5 visíveis).

SRP: Única responsabilidade - validar regras de compra de cartas abertas.

Regras validadas:
- Índice deve ser válido (0-4)
- Locomotiva só pode ser comprada como primeira carta do turno
- Não pode comprar mais de 2 cartas normais por turno
- Locomotiva conta como turno completo (2 cartas)
"""

from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from ...entities.carta_vagao import CartaVagao


@dataclass
class CompraAbertaValidationResult:
    """
    Resultado da validação de compra de carta aberta.
    
    Attributes:
        valido: Se a compra é permitida
        erro: Mensagem de erro (se inválido)
        carta: Carta que seria comprada (se índice válido)
    """
    valido: bool
    erro: Optional[str] = None
    carta: Optional['CartaVagao'] = None
    
    @property
    def invalido(self) -> bool:
        """Conveniência para verificar se é inválido."""
        return not self.valido


class CartaAbertaValidator:
    """
    Valida se compra de carta aberta é permitida.
    
    Regras de validação:
    1. Índice deve estar entre 0-4
    2. Se for locomotiva: só pode ser primeira carta do turno
    3. Se for carta normal: não pode ter completado turno
    
    SRP: Apenas valida regras de compra aberta.
    
    Exemplo de uso:
        validator = CartaAbertaValidator(estado_compra, gerenciador_baralho)
        resultado = validator.validar(indice=2)
        if resultado.invalido:
            return error_response(resultado.erro)
        carta = resultado.carta
    """
    
    def __init__(self, estado_compra, gerenciador_baralho):
        """
        Inicializa validator com dependências.
        
        Args:
            estado_compra: Estado atual de compras do turno
            gerenciador_baralho: Gerenciador do baralho de vagões
        """
        self._estado_compra = estado_compra
        self._gerenciador_baralho = gerenciador_baralho
    
    def validar(self, indice: int) -> CompraAbertaValidationResult:
        """
        Valida compra de carta aberta por índice.
        
        Executa validações em ordem:
        1. Índice válido?
        2. Regras de compra permitem esta carta?
        
        Args:
            indice: Índice da carta nas cartas abertas (0-4)
            
        Returns:
            CompraAbertaValidationResult com carta se válido
        """
        # Validar índice
        resultado_indice = self._validar_indice(indice)
        if resultado_indice.invalido:
            return resultado_indice
        
        # Obter carta do índice
        carta = self._obter_carta(indice)
        
        # Validar regras de compra para esta carta específica
        resultado_regras = self._validar_regras_compra(carta)
        if resultado_regras.invalido:
            return resultado_regras
        
        return CompraAbertaValidationResult(valido=True, carta=carta)
    
    def _validar_indice(self, indice: int) -> CompraAbertaValidationResult:
        """
        Valida se índice é válido (0 a len(cartas_abertas)-1).
        """
        cartas_abertas = self._gerenciador_baralho.obterCartasAbertas()
        
        if indice < 0:
            return CompraAbertaValidationResult(
                valido=False,
                erro=f"Índice {indice} inválido. Deve ser maior ou igual a 0"
            )
        
        if indice >= len(cartas_abertas):
            return CompraAbertaValidationResult(
                valido=False,
                erro=f"Índice {indice} inválido. "
                     f"Deve estar entre 0 e {len(cartas_abertas) - 1}"
            )
        
        return CompraAbertaValidationResult(valido=True)
    
    def _obter_carta(self, indice: int) -> 'CartaVagao':
        """Obtém carta do índice especificado."""
        return self._gerenciador_baralho.obterCartasAbertas()[indice]
    
    def _validar_regras_compra(self, carta: 'CartaVagao') -> CompraAbertaValidationResult:
        """
        Valida regras de compra para a carta específica.
        
        Regras:
        - Locomotiva: só pode ser comprada como primeira carta
        - Carta normal: não pode exceder 2 cartas por turno
        """
        eh_locomotiva = getattr(carta, 'ehLocomotiva', False)
        
        if not self._estado_compra.podeComprarCartaAberta(ehLocomotiva=eh_locomotiva):
            return CompraAbertaValidationResult(
                valido=False,
                erro=self._estado_compra.obterMensagemStatus()
            )
        
        return CompraAbertaValidationResult(valido=True)
    
    def validar_locomotiva_especifica(self, indice: int) -> CompraAbertaValidationResult:
        """
        Valida se pode comprar locomotiva especificamente.
        
        Método auxiliar para verificações específicas de locomotiva.
        
        Args:
            indice: Índice da carta
            
        Returns:
            CompraAbertaValidationResult
        """
        resultado = self._validar_indice(indice)
        if resultado.invalido:
            return resultado
        
        carta = self._obter_carta(indice)
        
        if not carta.ehLocomotiva:
            return CompraAbertaValidationResult(
                valido=False,
                erro=f"Carta no índice {indice} não é uma locomotiva"
            )
        
        return self._validar_regras_compra(carta)

    def tem_carta_compravel(self) -> bool:
        """
        Verifica se há alguma carta aberta que pode ser comprada.
        
        Usado por CompraValidator.ha_opcao_de_compra() para delegar lógica.
        
        Returns:
            True se existe pelo menos uma carta aberta comprável
        """
        cartas_abertas = self._gerenciador_baralho.obterCartasAbertas()
        
        for carta in cartas_abertas:
            eh_locomotiva = getattr(carta, 'ehLocomotiva', False)
            if self._estado_compra.podeComprarCartaAberta(ehLocomotiva=eh_locomotiva):
                return True
        
        return False
