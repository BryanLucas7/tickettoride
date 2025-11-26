"""
Interface base para estratégias de validação de conquista de rotas.

GoF Pattern: Strategy
- Define interface comum para todas as estratégias de validação
- Permite adicionar novas estratégias sem modificar clientes

GRASP: Protected Variations
- Protege contra variações nas regras de validação

Refatoração SRP:
- Interface base neste arquivo
- RotaColoridaStrategy em rota_colorida_strategy.py
- RotaCinzaStrategy em rota_cinza_strategy.py
- Factory em rota_validation_factory.py

Uso:
    from .rota_validation_factory import criar_estrategia_validacao
    
    estrategia = criar_estrategia_validacao(rota.cor)
    resultado = estrategia.validar(cartas_jogador, comprimento, cor_rota)
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
from app.core.domain.entities.carta_vagao import CartaVagao
from app.core.domain.entities.cor import Cor


class RotaValidationStrategy(ABC):
    """Interface base para estratégias de validação de rota.
    
    Strategy Pattern: Define interface comum para todas as estratégias.
    
    Refatoração DRY: Método _montar_cartas_usadas implementado na base
    para eliminar duplicação nas subclasses.
    
    Implementações:
    - RotaColoridaStrategy: Para rotas com cor específica
    - RotaCinzaStrategy: Para rotas cinzas (qualquer cor)
    """
    
    @abstractmethod
    def validar(self, cartas_jogador: List[CartaVagao], comprimento: int, cor_rota: Cor) -> Dict:
        """Valida se as cartas do jogador são suficientes para conquistar a rota.
        
        Args:
            cartas_jogador: Lista de cartas que o jogador possui
            comprimento: Comprimento da rota (número de cartas necessárias)
            cor_rota: Cor da rota (ou CINZA para rotas cinzas)
            
        Returns:
            Dict com:
                - valido: bool - Se as cartas são válidas
                - mensagem: str - Mensagem descritiva
                - cartas_usadas: List[CartaVagao] - Cartas que seriam usadas (se válido)
        """
        pass
    
    def _montar_cartas_usadas(
        self, 
        cartas_cor: List[CartaVagao], 
        locomotivas: List[CartaVagao], 
        comprimento: int
    ) -> Tuple[List[CartaVagao], int, int]:
        """
        Monta lista de cartas a usar, priorizando cartas da cor.
        
        DRY: Método extraído para eliminar duplicação entre estratégias.
        
        Args:
            cartas_cor: Cartas da cor desejada
            locomotivas: Cartas locomotiva disponíveis
            comprimento: Quantidade total de cartas necessárias
            
        Returns:
            Tupla (cartas_usadas, qtd_cor_usadas, qtd_locomotivas_usadas)
        """
        cartas_usadas: List[CartaVagao] = []
        
        # Prioriza cartas da cor
        cartas_cor_necessarias = min(len(cartas_cor), comprimento)
        cartas_usadas.extend(cartas_cor[:cartas_cor_necessarias])
        
        # Completa com locomotivas se necessário
        locomotivas_necessarias = comprimento - cartas_cor_necessarias
        cartas_usadas.extend(locomotivas[:locomotivas_necessarias])
        
        return cartas_usadas, cartas_cor_necessarias, locomotivas_necessarias


# Re-exports para compatibilidade com imports existentes
from .rota_colorida_strategy import RotaColoridaStrategy
from .rota_cinza_strategy import RotaCinzaStrategy

__all__ = ['RotaValidationStrategy', 'RotaColoridaStrategy', 'RotaCinzaStrategy']
