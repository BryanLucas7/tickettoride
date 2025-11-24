from dataclasses import dataclass, field
from typing import List
from .carta_vagao import CartaVagao
from ..support.card_helpers import remover_cartas_por_cores as helper_remover_cartas

@dataclass
class Mao:
    cartasVagao: List[CartaVagao] = field(default_factory=list)

    def adicionarCarta(self, carta: CartaVagao):
        """Adiciona uma carta à mão"""
        self.cartasVagao.append(carta)

    def removerCartas(self, cartas: List[CartaVagao]) -> bool:
        """Remove as cartas especificadas da mão
        
        Returns:
            True se todas as cartas foram removidas com sucesso
        """
        for c in cartas:
            if c not in self.cartasVagao:
                return False
        for c in cartas:
            self.cartasVagao.remove(c)
        return True

    def getQuantidade(self, cor=None) -> int:
        """Retorna a quantidade de cartas na mão
        
        Args:
            cor: Se especificado, conta apenas cartas dessa cor
        """
        if cor is None:
            return len(self.cartasVagao)
        return sum(1 for c in self.cartasVagao if c.cor == cor and not c.ehLocomotiva)
    
    def remover_cartas_por_cores(self, cores: List[str]) -> List[CartaVagao]:
        """Remove e retorna cartas específicas da mão baseado nas cores fornecidas.
        
        Usa CardHelpers centralizado para eliminar duplicação de código.
        
        Args:
            cores: Lista de cores das cartas a remover (ex: ["azul", "locomotiva", "vermelho"])
        
        Returns:
            Lista de CartaVagao que foram removidas da mão
            
        Raises:
            ValueError: Se alguma carta da cor especificada não for encontrada na mão
            
        Example:
            >>> mao.remover_cartas_por_cores(["azul", "locomotiva"])
            [CartaVagao(cor="azul"), CartaVagao(ehLocomotiva=True)]
        """
        try:
            # Delega para CardHelpers que implementa a lógica de busca/remoção
            cartas_removidas = helper_remover_cartas(self.cartasVagao, cores)
            return cartas_removidas
        except ValueError as e:
            # Re-lança com mensagem específica do contexto
            raise ValueError(f"Erro ao remover cartas da mão: {str(e)}")
