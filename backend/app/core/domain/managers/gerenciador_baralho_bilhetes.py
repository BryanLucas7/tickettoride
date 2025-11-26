"""
Gerenciador do Baralho de Bilhetes de Destino.

Padrão GRASP: Information Expert - possui os dados dos bilhetes
Padrão GRASP: Pure Fabrication - separa responsabilidade de vagões e bilhetes
Princípio SRP: Gerencia APENAS bilhetes de destino
"""

from dataclasses import dataclass, field
from typing import List

from ..entities.baralho import Baralho
from ..entities.bilhete_destino import BilheteDestino, BILHETES_DESTINO


@dataclass
class GerenciadorBaralhoBilhetes:
    """
    Gerencia o baralho de bilhetes de destino.
    
    Responsabilidades (SRP):
    - Inicializar o baralho com os 30 bilhetes
    - Comprar bilhetes do baralho
    - Devolver bilhetes recusados
    
    Extraído de GerenciadorBaralhoVagoes para respeitar SRP.
    """
    baralhoBilhetes: Baralho = field(default_factory=Baralho)
    
    def __post_init__(self):
        """Inicializa o baralho de bilhetes após criação."""
        self.inicializar()
    
    def inicializar(self) -> None:
        """
        Cria o baralho com os 30 bilhetes de destino do jogo.
        
        Usa BILHETES_DESTINO predefinidos em bilhete_destino.py.
        """
        for bilhete in BILHETES_DESTINO:
            self.baralhoBilhetes.adicionar(bilhete)
        
        self.baralhoBilhetes.embaralhar()
        print(f"[OK] Baralho de bilhetes criado: {len(self.baralhoBilhetes.cartas)} bilhetes")
    
    def comprar(self, quantidade: int = 3) -> List[BilheteDestino]:
        """
        Compra bilhetes de destino do baralho.
        
        Args:
            quantidade: Número de bilhetes a comprar (padrão: 3)
            
        Returns:
            Lista com os bilhetes comprados
        """
        bilhetes = []
        for _ in range(quantidade):
            bilhete = self.baralhoBilhetes.comprar()
            if bilhete:
                bilhetes.append(bilhete)
        return bilhetes
    
    def devolver(self, bilhetes: List[BilheteDestino]) -> None:
        """
        Devolve bilhetes não aceitos ao fundo do baralho.
        
        Args:
            bilhetes: Lista de bilhetes a serem devolvidos
        """
        for bilhete in bilhetes:
            self.baralhoBilhetes.adicionar(bilhete, endOf=True)
    
    @property
    def quantidade_restante(self) -> int:
        """Retorna quantidade de bilhetes restantes no baralho."""
        return len(self.baralhoBilhetes.cartas)
