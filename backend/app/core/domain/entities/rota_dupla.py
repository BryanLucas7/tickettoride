"""
RotaDupla - Entidade que representa um par de rotas paralelas.

Padrão GRASP: Information Expert
- Conhece as duas rotas paralelas
- Responsável apenas por representação do par (imutável)

Separado do validador para aderir ao SRP.
"""

from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .rota import Rota


@dataclass
class RotaDupla:
    """
    Representa um par de rotas paralelas entre duas cidades.
    
    GRASP Information Expert: Conhece as duas rotas paralelas.
    SRP: Responsável apenas por consultas, não modifica estado.
    """
    
    rota1: 'Rota'
    rota2: 'Rota'
    
    def obter_rota_disponivel(self) -> Optional['Rota']:
        """Retorna rota disponível (não conquistada).
        
        Returns:
            Rota disponível ou None se ambas conquistadas/bloqueadas
        """
        if not self.rota1.proprietario:
            return self.rota1
        if not self.rota2.proprietario:
            return self.rota2
        return None
    
    def obter_rota_conquistada(self) -> Optional['Rota']:
        """Retorna rota já conquistada.
        
        Returns:
            Rota conquistada ou None se nenhuma foi conquistada
        """
        if self.rota1.proprietario:
            return self.rota1
        if self.rota2.proprietario:
            return self.rota2
        return None
    
    def obter_rota_paralela(self, rota: 'Rota') -> Optional['Rota']:
        """Retorna a rota paralela à rota informada.
        
        Args:
            rota: Uma das rotas do par
            
        Returns:
            A outra rota do par, ou None se rota não pertence ao par
        """
        if self.rota1.id == rota.id:
            return self.rota2
        elif self.rota2.id == rota.id:
            return self.rota1
        return None
    
    def contem_rota(self, rota: 'Rota') -> bool:
        """Verifica se a rota pertence a este par.
        
        Args:
            rota: Rota a verificar
            
        Returns:
            True se rota pertence ao par
        """
        return self.rota1.id == rota.id or self.rota2.id == rota.id
    
    def ambas_disponiveis(self) -> bool:
        """Verifica se ambas as rotas estão disponíveis."""
        return not self.rota1.proprietario and not self.rota2.proprietario
    
    def alguma_conquistada(self) -> bool:
        """Verifica se alguma rota do par foi conquistada."""
        return bool(self.rota1.proprietario or self.rota2.proprietario)
