"""
Estado de compra de cartas durante um turno

Gerencia as regras de compra:
- Jogador pode comprar 2 cartas normalmente
- Se comprar locomotiva das cartas abertas, só pode comprar 1 (termina o turno)
- Cartas do baralho fechado sempre contam como 1 compra normal

Aplica GRASP Information Expert: EstadoCompra conhece as regras de compra
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class EstadoCompraCartas:
    """Gerencia estado de compra de cartas durante um turno
    
    Attributes:
        cartasCompradas: Número de cartas já compradas neste turno
        comprouLocomotivaDasAbertas: Se comprou locomotiva das cartas abertas
        turnoCompleto: Se o turno de compra está completo
    """
    cartasCompradas: int = 0
    comprouLocomotivaDasAbertas: bool = False
    turnoCompleto: bool = False
    
    def podeComprarCartaAberta(self, ehLocomotiva: bool) -> bool:
        """Verifica se pode comprar uma carta aberta
        
        Args:
            ehLocomotiva: Se a carta que deseja comprar é locomotiva
            
        Returns:
            True se pode comprar
        """
        # Se turno já está completo, não pode comprar mais
        if self.turnoCompleto:
            return False
        
        # Se já comprou locomotiva das abertas, não pode comprar mais
        if self.comprouLocomotivaDasAbertas:
            return False
        
        # Se é locomotiva e já comprou 1 carta, não pode
        if ehLocomotiva and self.cartasCompradas >= 1:
            return False
        
        # Se já comprou 2 cartas, não pode comprar mais
        if self.cartasCompradas >= 2:
            return False
        
        return True
    
    def podeComprarCartaFechada(self) -> bool:
        """Verifica se pode comprar do baralho fechado
        
        Returns:
            True se pode comprar
        """
        # Se turno já está completo, não pode comprar mais
        if self.turnoCompleto:
            return False
        
        # Se já comprou locomotiva das abertas, não pode comprar mais
        if self.comprouLocomotivaDasAbertas:
            return False
        
        # Se já comprou 2 cartas, não pode comprar mais
        if self.cartasCompradas >= 2:
            return False
        
        return True
    
    def registrarCompraCartaAberta(self, ehLocomotiva: bool):
        """Registra compra de carta aberta
        
        Args:
            ehLocomotiva: Se a carta comprada é locomotiva
        """
        self.cartasCompradas += 1
        
        # Se comprou locomotiva, marca flag e completa turno
        if ehLocomotiva:
            self.comprouLocomotivaDasAbertas = True
            self.turnoCompleto = True
        # Se comprou 2 cartas, completa turno
        elif self.cartasCompradas >= 2:
            self.turnoCompleto = True
    
    def registrarCompraCartaFechada(self):
        """Registra compra de carta do baralho fechado"""
        self.cartasCompradas += 1
        
        # Se comprou 2 cartas, completa turno
        if self.cartasCompradas >= 2:
            self.turnoCompleto = True
    
    def resetar(self):
        """Reseta estado para novo turno"""
        self.cartasCompradas = 0
        self.comprouLocomotivaDasAbertas = False
        self.turnoCompleto = False
    
    def obterMensagemStatus(self) -> str:
        """Retorna mensagem descritiva do estado atual
        
        Returns:
            Mensagem descrevendo o estado
        """
        if self.turnoCompleto:
            if self.comprouLocomotivaDasAbertas:
                return "Turno completo: comprou locomotiva das cartas abertas"
            else:
                return f"Turno completo: comprou {self.cartasCompradas} cartas"
        
        cartasRestantes = 2 - self.cartasCompradas
        
        if self.comprouLocomotivaDasAbertas:
            return "Não pode comprar mais: já comprou locomotiva das cartas abertas"
        
        if cartasRestantes == 2:
            return "Pode comprar 2 cartas (ou 1 locomotiva aberta)"
        elif cartasRestantes == 1:
            return "Pode comprar mais 1 carta (exceto locomotiva aberta)"
        else:
            return "Não pode comprar mais cartas neste turno"
