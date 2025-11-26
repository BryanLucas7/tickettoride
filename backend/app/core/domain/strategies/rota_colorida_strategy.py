"""
Estratégia de validação para rotas com cor específica.

GoF Pattern: Strategy
- Implementa algoritmo de validação para rotas coloridas

Regras:
- Precisa de N cartas da cor da rota (onde N = comprimento)
- Locomotivas podem ser usadas como coringa
- Pode usar apenas locomotivas
- Não pode usar cartas de outras cores

Refatoração SRP: Extraído de rota_validation_strategy.py para
separar cada estratégia em seu próprio arquivo.
"""

from typing import List, Dict
from app.core.domain.entities.carta_vagao import CartaVagao
from app.core.domain.entities.cor import Cor
from .rota_validation_strategy import RotaValidationStrategy


class RotaColoridaStrategy(RotaValidationStrategy):
    """Estratégia para validar rotas com cor específica.
    
    Regras:
    - Precisa de N cartas da cor da rota (onde N = comprimento)
    - Locomotivas podem ser usadas como coringa
    - Pode usar apenas locomotivas
    - Não pode usar cartas de outras cores
    
    Exemplo:
        >>> strategy = RotaColoridaStrategy()
        >>> resultado = strategy.validar(cartas, comprimento=3, cor_rota=Cor.VERMELHO)
        >>> if resultado["valido"]:
        ...     cartas_usadas = resultado["cartas_usadas"]
    """
    
    def validar(self, cartas_jogador: List[CartaVagao], comprimento: int, cor_rota: Cor) -> Dict:
        """Valida conquista de rota colorida.
        
        Args:
            cartas_jogador: Lista de cartas que o jogador possui
            comprimento: Comprimento da rota (número de cartas necessárias)
            cor_rota: Cor da rota a ser conquistada
            
        Returns:
            Dict com:
                - valido: bool - Se as cartas são válidas
                - mensagem: str - Mensagem descritiva
                - cartas_usadas: List[CartaVagao] - Cartas que seriam usadas (se válido)
        """
        # Separa cartas por tipo
        cartas_da_cor = [c for c in cartas_jogador if c.cor == cor_rota and not c.ehLocomotiva]
        locomotivas = [c for c in cartas_jogador if c.ehLocomotiva]
        
        total_cartas_da_cor = len(cartas_da_cor)
        total_locomotivas = len(locomotivas)
        
        # Verifica se tem cartas suficientes (cor + locomotivas)
        total_disponiveis = total_cartas_da_cor + total_locomotivas
        
        if total_disponiveis < comprimento:
            return {
                "valido": False,
                "mensagem": f"Cartas insuficientes: tem {total_cartas_da_cor} {cor_rota.value} + {total_locomotivas} locomotivas, precisa de {comprimento}",
                "cartas_usadas": []
            }
        
        # Monta lista de cartas usando método da classe base (DRY)
        cartas_usadas, cartas_cor_usadas, locomotivas_usadas = self._montar_cartas_usadas(
            cartas_da_cor, locomotivas, comprimento
        )
        
        return {
            "valido": True,
            "mensagem": f"Válido: {cartas_cor_usadas} {cor_rota.value} + {locomotivas_usadas} locomotivas",
            "cartas_usadas": cartas_usadas
        }
