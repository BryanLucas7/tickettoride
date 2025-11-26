"""
Regra de reset de cartas abertas quando 3+ locomotivas aparecem.

GoF Pattern: Strategy
GRASP: Pure Fabrication

Regra oficial do Ticket to Ride:
"Se 3 ou mais locomotivas aparecerem nas 5 cartas abertas,
todas são descartadas e 5 novas cartas são reveladas."

Refatoração SRP:
- Extraída de GerenciadorBaralhoVagoes._verificarLocomotivas()
- Permite testar a regra isoladamente
- Permite injetar regras diferentes (NullResetRule para testes)
"""

from typing import List, Protocol, runtime_checkable

from ..entities.carta_vagao import CartaVagao


@runtime_checkable
class CartasAbertasRule(Protocol):
    """
    Interface (Protocol) para regras de cartas abertas.
    
    Strategy Pattern: Define contrato para diferentes estratégias
    de verificação de cartas abertas.
    """
    
    def deve_resetar(self, cartas_abertas: List[CartaVagao]) -> bool:
        """
        Verifica se as cartas abertas devem ser resetadas.
        
        Args:
            cartas_abertas: Lista de cartas visíveis na mesa
            
        Returns:
            True se deve resetar, False caso contrário
        """
        ...


class LocomotivaResetRule:
    """
    Regra que verifica se 3+ locomotivas estão abertas.
    
    SRP: Única responsabilidade - verificar condição de reset por locomotivas.
    
    Regra oficial:
    - Se 3 ou mais locomotivas aparecerem nas 5 cartas abertas
    - Todas as cartas são descartadas
    - 5 novas cartas são reveladas
    - O processo se repete até ter menos de 3 locomotivas
    
    Exemplo de uso:
        rule = LocomotivaResetRule()
        if rule.deve_resetar(cartas_abertas):
            # Executar reset das cartas
    """
    
    LIMITE_LOCOMOTIVAS: int = 3
    
    def deve_resetar(self, cartas_abertas: List[CartaVagao]) -> bool:
        """
        Verifica se há 3+ locomotivas nas cartas abertas.
        
        Args:
            cartas_abertas: Lista de cartas visíveis na mesa
            
        Returns:
            True se deve resetar (3+ locomotivas), False caso contrário
        """
        if not cartas_abertas:
            return False
        
        locomotivas = self._contar_locomotivas(cartas_abertas)
        return locomotivas >= self.LIMITE_LOCOMOTIVAS
    
    def _contar_locomotivas(self, cartas: List[CartaVagao]) -> int:
        """
        Conta o número de locomotivas em uma lista de cartas.
        
        Args:
            cartas: Lista de cartas a verificar
            
        Returns:
            Número de locomotivas encontradas
        """
        return sum(1 for carta in cartas if carta.ehLocomotiva)
    
    def obter_contagem_locomotivas(self, cartas_abertas: List[CartaVagao]) -> int:
        """
        Retorna a contagem de locomotivas (útil para logs/debug).
        
        Args:
            cartas_abertas: Lista de cartas visíveis
            
        Returns:
            Número de locomotivas
        """
        return self._contar_locomotivas(cartas_abertas)


class NullResetRule:
    """
    Regra nula que nunca reseta (Null Object Pattern).
    
    Útil para:
    - Testes unitários onde não queremos reset automático
    - Desabilitar a regra temporariamente
    - Cenários de debug
    
    Exemplo:
        gerenciador = GerenciadorBaralhoVagoes(reset_rule=NullResetRule())
        # Nunca vai resetar automaticamente
    """
    
    def deve_resetar(self, cartas_abertas: List[CartaVagao]) -> bool:
        """Sempre retorna False - nunca reseta."""
        return False


class CustomThresholdRule:
    """
    Regra com threshold customizável (extensibilidade).
    
    Permite configurar um limite diferente de locomotivas
    para cenários especiais ou variantes do jogo.
    
    Exemplo:
        # Resetar se 2+ locomotivas (mais restritivo)
        rule = CustomThresholdRule(limite=2)
    """
    
    def __init__(self, limite: int = 3):
        """
        Inicializa com limite customizado.
        
        Args:
            limite: Número mínimo de locomotivas para reset (default: 3)
        """
        self.limite = limite
    
    def deve_resetar(self, cartas_abertas: List[CartaVagao]) -> bool:
        """Verifica se há locomotivas >= limite."""
        if not cartas_abertas:
            return False
        
        locomotivas = sum(1 for carta in cartas_abertas if carta.ehLocomotiva)
        return locomotivas >= self.limite
