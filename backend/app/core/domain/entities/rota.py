from dataclasses import dataclass
from .cidade import Cidade
from .cor import Cor
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .jogador import Jogador

@dataclass
class Rota:
    id: str
    cidadeA: Cidade
    cidadeB: Cidade
    cor: Cor
    comprimento: int
    proprietario: Optional['Jogador'] = None
    ehConcluida: bool = False

    def reivindicarRota(self, proprietario: 'Jogador', cartas: List) -> bool:
        """Reivindica a rota para um jogador
        
        Args:
            proprietario: Jogador que está reivindicando a rota
            cartas: Lista de cartas usadas para reivindicar
            
        Returns:
            True se a rota foi reivindicada com sucesso
        """
        if self.proprietario is not None:
            return False
        
        # Validação: exige quantidade de cartas igual ao comprimento
        if len(cartas) < self.comprimento:
            return False
        
        self.proprietario = proprietario
        self.ehConcluida = True
        return True
