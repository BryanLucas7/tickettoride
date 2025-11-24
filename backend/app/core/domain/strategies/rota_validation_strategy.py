"""
Strategy Pattern para validação de conquista de rotas

Implementa diferentes estratégias de validação:
- RotaColoridaStrategy: Valida rotas com cor específica
- RotaCinzaStrategy: Valida rotas cinzas (qualquer cor)

Aplica padrões:
- GoF Strategy Pattern: Encapsula algoritmos de validação
- GRASP Protected Variations: Protege contra variações nas regras
"""

from abc import ABC, abstractmethod
from typing import List, Dict
from app.core.domain.entities.carta_vagao import CartaVagao
from app.core.domain.entities.cor import Cor

class RotaValidationStrategy(ABC):
    """Interface base para estratégias de validação de rota
    
    Strategy Pattern: Define interface comum para todas as estratégias
    """
    
    @abstractmethod
    def validar(self, cartas_jogador: List[CartaVagao], comprimento: int, cor_rota: Cor) -> Dict:
        """Valida se as cartas do jogador são suficientes para conquistar a rota
        
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


class RotaColoridaStrategy(RotaValidationStrategy):
    """Estratégia para validar rotas com cor específica
    
    Regras:
    - Precisa de N cartas da cor da rota (onde N = comprimento)
    - Locomotivas podem ser usadas como coringa
    - Pode usar apenas locomotivas
    - Não pode usar cartas de outras cores
    """
    
    def validar(self, cartas_jogador: List[CartaVagao], comprimento: int, cor_rota: Cor) -> Dict:
        """Valida conquista de rota colorida"""
        
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
        
        # Monta lista de cartas a usar (prioriza cartas da cor, depois locomotivas)
        cartas_usadas = []
        
        # Usa cartas da cor primeiro
        cartas_cor_necessarias = min(total_cartas_da_cor, comprimento)
        cartas_usadas.extend(cartas_da_cor[:cartas_cor_necessarias])
        
        # Completa com locomotivas se necessário
        locomotivas_necessarias = comprimento - cartas_cor_necessarias
        cartas_usadas.extend(locomotivas[:locomotivas_necessarias])
        
        return {
            "valido": True,
            "mensagem": f"Válido: {cartas_cor_necessarias} {cor_rota.value} + {locomotivas_necessarias} locomotivas",
            "cartas_usadas": cartas_usadas
        }


class RotaCinzaStrategy(RotaValidationStrategy):
    """Estratégia para validar rotas cinzas (qualquer cor)
    
    Regras:
    - Precisa de N cartas da MESMA cor (onde N = comprimento)
    - Pode escolher qualquer cor que tenha quantidade suficiente
    - Locomotivas podem ser usadas como coringa
    - Pode usar apenas locomotivas
    """
    
    def validar(self, cartas_jogador: List[CartaVagao], comprimento: int, cor_rota: Cor = None) -> Dict:
        """Valida conquista de rota cinza"""
        
        # Separa locomotivas
        locomotivas = [c for c in cartas_jogador if c.ehLocomotiva]
        total_locomotivas = len(locomotivas)
        
        # Conta cartas por cor (exceto locomotivas)
        cartas_por_cor: Dict[Cor, List[CartaVagao]] = {}
        for carta in cartas_jogador:
            if not carta.ehLocomotiva:
                if carta.cor not in cartas_por_cor:
                    cartas_por_cor[carta.cor] = []
                cartas_por_cor[carta.cor].append(carta)
        
        # Procura cor com quantidade suficiente (incluindo locomotivas)
        cores_validas = []
        for cor, cartas_cor in cartas_por_cor.items():
            total_com_locomotivas = len(cartas_cor) + total_locomotivas
            if total_com_locomotivas >= comprimento:
                cores_validas.append((cor, cartas_cor))
        
        # Se não tem nenhuma cor válida, verifica se apenas locomotivas é suficiente
        if not cores_validas:
            if total_locomotivas >= comprimento:
                return {
                    "valido": True,
                    "mensagem": f"Válido: {comprimento} locomotivas",
                    "cartas_usadas": locomotivas[:comprimento]
                }
            return {
                "valido": False,
                "mensagem": f"Cartas insuficientes: precisa de {comprimento} cartas da mesma cor (+locomotivas). Tem {total_locomotivas} locomotivas.",
                "cartas_usadas": []
            }
        
        # Escolhe a melhor cor (a que tem mais cartas, para economizar locomotivas)
        melhor_cor, cartas_melhor_cor = max(cores_validas, key=lambda x: len(x[1]))
        
        # Monta lista de cartas a usar
        cartas_usadas = []
        
        # Usa cartas da cor escolhida primeiro
        cartas_cor_necessarias = min(len(cartas_melhor_cor), comprimento)
        cartas_usadas.extend(cartas_melhor_cor[:cartas_cor_necessarias])
        
        # Completa com locomotivas se necessário
        locomotivas_necessarias = comprimento - cartas_cor_necessarias
        cartas_usadas.extend(locomotivas[:locomotivas_necessarias])
        
        return {
            "valido": True,
            "mensagem": f"Válido: {cartas_cor_necessarias} {melhor_cor.value} + {locomotivas_necessarias} locomotivas",
            "cartas_usadas": cartas_usadas
        }


def criar_estrategia_validacao(cor_rota: Cor) -> RotaValidationStrategy:
    """Factory method para criar estratégia apropriada
    
    Args:
        cor_rota: Cor da rota (CINZA para rotas cinzas)
        
    Returns:
        Estratégia apropriada para validar a rota
    """
    if cor_rota == Cor.CINZA:
        return RotaCinzaStrategy()
    else:
        return RotaColoridaStrategy()
