"""
Validador de compra de carta do baralho fechado.

SRP: Única responsabilidade - validar regras de compra do baralho fechado.

Regras validadas:
- Não pode ter comprado locomotiva das abertas neste turno
- Não pode ter completado o turno (2 cartas já compradas)
- Baralho deve ter cartas disponíveis (ou descarte para reabastecer)
"""

from typing import Optional
from dataclasses import dataclass


@dataclass
class CompraFechadaValidationResult:
    """
    Resultado da validação de compra de carta fechada.
    
    Attributes:
        valido: Se a compra é permitida
        erro: Mensagem de erro (se inválido)
    """
    valido: bool
    erro: Optional[str] = None
    
    @property
    def invalido(self) -> bool:
        """Conveniência para verificar se é inválido."""
        return not self.valido


class CartaFechadaValidator:
    """
    Valida se compra de carta do baralho fechado é permitida.
    
    Regras de validação:
    1. Estado de compra deve permitir (não comprou locomotiva, turno não completo)
    2. Baralho deve ter cartas disponíveis
    
    SRP: Apenas valida regras de compra fechada.
    
    Exemplo de uso:
        validator = CartaFechadaValidator(estado_compra, gerenciador_baralho)
        resultado = validator.validar()
        if resultado.invalido:
            return error_response(resultado.erro)
    """
    
    def __init__(self, estado_compra, gerenciador_baralho):
        """
        Inicializa validator com dependências.
        
        Args:
            estado_compra: Estado atual de compras do turno (EstadoCompraCartas)
            gerenciador_baralho: Gerenciador do baralho de vagões
        """
        self._estado_compra = estado_compra
        self._gerenciador_baralho = gerenciador_baralho
    
    def validar(self) -> CompraFechadaValidationResult:
        """
        Valida se compra de carta fechada é permitida.
        
        Executa validações em ordem:
        1. Estado de compra permite?
        2. Há cartas disponíveis?
        
        Returns:
            CompraFechadaValidationResult
        """
        # Validar estado de compra
        resultado_estado = self._validar_estado_compra()
        if resultado_estado.invalido:
            return resultado_estado
        
        # Validar disponibilidade de cartas
        resultado_disponibilidade = self._validar_disponibilidade()
        if resultado_disponibilidade.invalido:
            return resultado_disponibilidade
        
        return CompraFechadaValidationResult(valido=True)
    
    def _validar_estado_compra(self) -> CompraFechadaValidationResult:
        """
        Valida se o estado de compra permite comprar carta fechada.
        
        Regras:
        - Não pode ter comprado locomotiva das abertas
        - Turno não pode estar completo (2 cartas)
        """
        if not self._estado_compra.podeComprarCartaFechada():
            return CompraFechadaValidationResult(
                valido=False,
                erro=self._estado_compra.obterMensagemStatus()
            )
        return CompraFechadaValidationResult(valido=True)
    
    def _validar_disponibilidade(self) -> CompraFechadaValidationResult:
        """
        Valida se há cartas disponíveis no baralho ou descarte.
        """
        if not self._tem_cartas_disponiveis():
            return CompraFechadaValidationResult(
                valido=False,
                erro="Baralho vazio e sem cartas no descarte para reabastecer"
            )
        return CompraFechadaValidationResult(valido=True)
    
    def _tem_cartas_disponiveis(self) -> bool:
        """
        Verifica se há cartas no baralho ou no descarte.
        
        Returns:
            True se há cartas disponíveis para compra
        """
        baralho = self._gerenciador_baralho.baralhoVagoes
        
        # Tem cartas no baralho?
        if baralho and len(baralho.cartas) > 0:
            return True
        
        # Tem cartas no descarte para reabastecer?
        return bool(self._gerenciador_baralho.descarteVagoes)

    def pode_comprar(self) -> bool:
        """
        Verifica se é possível comprar carta fechada neste momento.
        
        Combina validação de estado + disponibilidade.
        Usado por CompraValidator.ha_opcao_de_compra() para delegar lógica.
        
        Returns:
            True se pode comprar carta fechada
        """
        # Estado permite?
        if not self._estado_compra.podeComprarCartaFechada():
            return False
        
        # Há cartas disponíveis?
        return self._tem_cartas_disponiveis()
