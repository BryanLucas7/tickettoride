"""
Estratégia de validação para rotas cinzas (qualquer cor).

GoF Pattern: Strategy
- Implementa algoritmo de validação para rotas cinzas

Regras:
- Precisa de N cartas da MESMA cor (onde N = comprimento)
- Pode escolher qualquer cor que tenha quantidade suficiente
- Locomotivas podem ser usadas como coringa
- Pode usar apenas locomotivas

Refatoração SRP: Extraído de rota_validation_strategy.py para
separar cada estratégia em seu próprio arquivo.
"""

from typing import List, Dict, Tuple
from app.core.domain.entities.carta_vagao import CartaVagao
from app.core.domain.entities.cor import Cor
from .rota_validation_strategy import RotaValidationStrategy


class RotaCinzaStrategy(RotaValidationStrategy):
    """Estratégia para validar rotas cinzas (qualquer cor).
    
    Regras:
    - Precisa de N cartas da MESMA cor (onde N = comprimento)
    - Pode escolher qualquer cor que tenha quantidade suficiente
    - Locomotivas podem ser usadas como coringa
    - Pode usar apenas locomotivas
    
    Refatoração SRP:
    - Métodos auxiliares extraídos para clareza e testabilidade
    - _separar_cartas_por_tipo: Separa locomotivas de cartas coloridas
    - _encontrar_cores_validas: Encontra cores com quantidade suficiente
    - _selecionar_melhor_opcao: Escolhe a melhor combinação de cartas
    
    Exemplo:
        >>> strategy = RotaCinzaStrategy()
        >>> resultado = strategy.validar(cartas, comprimento=4, cor_rota=Cor.CINZA)
        >>> if resultado["valido"]:
        ...     cartas_usadas = resultado["cartas_usadas"]
    """
    
    def validar(self, cartas_jogador: List[CartaVagao], comprimento: int, cor_rota: Cor = None) -> Dict:
        """
        Valida conquista de rota cinza.
        
        Pipeline refatorado para clareza:
        1. Separar cartas por tipo
        2. Encontrar cores válidas
        3. Selecionar melhor opção
        
        Args:
            cartas_jogador: Lista de cartas que o jogador possui
            comprimento: Comprimento da rota (número de cartas necessárias)
            cor_rota: Ignorado para rotas cinzas (qualquer cor é válida)
            
        Returns:
            Dict com:
                - valido: bool - Se as cartas são válidas
                - mensagem: str - Mensagem descritiva
                - cartas_usadas: List[CartaVagao] - Cartas que seriam usadas (se válido)
        """
        # Step 1: Separar cartas por tipo
        locomotivas, cartas_por_cor = self._separar_cartas_por_tipo(cartas_jogador)
        
        # Step 2: Encontrar cores válidas
        cores_validas = self._encontrar_cores_validas(cartas_por_cor, locomotivas, comprimento)
        
        # Step 3: Selecionar melhor opção
        return self._selecionar_melhor_opcao(cores_validas, locomotivas, comprimento)
    
    def _separar_cartas_por_tipo(
        self, 
        cartas: List[CartaVagao]
    ) -> Tuple[List[CartaVagao], Dict[Cor, List[CartaVagao]]]:
        """
        Separa cartas em locomotivas e por cor.
        
        SRP: Única responsabilidade - categorizar cartas.
        
        Args:
            cartas: Lista de cartas do jogador
            
        Returns:
            Tupla (locomotivas, dicionário_por_cor)
        """
        locomotivas = [c for c in cartas if c.ehLocomotiva]
        cartas_por_cor: Dict[Cor, List[CartaVagao]] = {}
        
        for carta in cartas:
            if not carta.ehLocomotiva:
                if carta.cor not in cartas_por_cor:
                    cartas_por_cor[carta.cor] = []
                cartas_por_cor[carta.cor].append(carta)
        
        return locomotivas, cartas_por_cor
    
    def _encontrar_cores_validas(
        self,
        cartas_por_cor: Dict[Cor, List[CartaVagao]],
        locomotivas: List[CartaVagao],
        comprimento: int
    ) -> List[Tuple[Cor, List[CartaVagao]]]:
        """
        Encontra cores com quantidade suficiente de cartas.
        
        SRP: Única responsabilidade - filtrar cores viáveis.
        
        Args:
            cartas_por_cor: Dicionário cor -> cartas
            locomotivas: Lista de locomotivas disponíveis
            comprimento: Quantidade de cartas necessárias
            
        Returns:
            Lista de tuplas (cor, cartas_dessa_cor) válidas
        """
        cores_validas = []
        total_locomotivas = len(locomotivas)
        
        for cor, cartas_cor in cartas_por_cor.items():
            total_com_locomotivas = len(cartas_cor) + total_locomotivas
            if total_com_locomotivas >= comprimento:
                cores_validas.append((cor, cartas_cor))
        
        return cores_validas
    
    def _selecionar_melhor_opcao(
        self,
        cores_validas: List[Tuple[Cor, List[CartaVagao]]],
        locomotivas: List[CartaVagao],
        comprimento: int
    ) -> Dict:
        """
        Seleciona a melhor opção de cartas para usar.
        
        SRP: Única responsabilidade - decidir quais cartas usar.
        
        Prioriza:
        1. Cor com mais cartas (economiza locomotivas)
        2. Apenas locomotivas se nenhuma cor válida
        
        Args:
            cores_validas: Cores que têm cartas suficientes
            locomotivas: Locomotivas disponíveis
            comprimento: Quantidade necessária
            
        Returns:
            Dict com resultado da validação
        """
        total_locomotivas = len(locomotivas)
        
        # Caso: apenas locomotivas
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
        
        # Escolher melhor cor (mais cartas para economizar locomotivas)
        melhor_cor, cartas_melhor_cor = max(cores_validas, key=lambda x: len(x[1]))
        
        # Montar cartas usando método da base (DRY)
        cartas_usadas, qtd_cor, qtd_loco = self._montar_cartas_usadas(
            cartas_melhor_cor, locomotivas, comprimento
        )
        
        return {
            "valido": True,
            "mensagem": f"Válido: {qtd_cor} {melhor_cor.value} + {qtd_loco} locomotivas",
            "cartas_usadas": cartas_usadas
        }
