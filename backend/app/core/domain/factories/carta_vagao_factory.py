"""
Factory para criação de cartas de vagão.

GoF Pattern: Factory Method
- Encapsula a criação de objetos CartaVagao
- Facilita testes e manutenção
- Centraliza regras de criação (cores, quantidades)

Refatoração SRP: Extraído de gerenciador_baralho_vagoes.py para
separar responsabilidade de criação da responsabilidade de gerenciamento.

Composição do baralho:
- 96 cartas normais (8 cores × 12 cartas)
- 14 locomotivas
- Total: 110 cartas
"""

from typing import List, Tuple
from ..entities.carta_vagao import CartaVagao
from ..entities.cor import Cor


class CartaVagaoFactory:
    """
    Factory Method Pattern para criação de cartas de vagão.
    
    Responsabilidade única (SRP): Criar cartas de vagão.
    Separa a lógica de criação da lógica de gerenciamento do baralho.
    
    GoF Pattern: Factory Method
    - Encapsula a criação de objetos CartaVagao
    - Facilita testes e manutenção
    - Centraliza regras de criação (cores, quantidades)
    
    Exemplo:
        >>> factory = CartaVagaoFactory()
        >>> carta = factory.criar_carta_normal(1, Cor.VERMELHO)
        >>> locomotiva = factory.criar_locomotiva(2)
        >>> baralho, _ = factory.criar_baralho_completo()
    """
    
    # Configuração das cartas - Protected Variations
    CORES_NORMAIS: List[Cor] = [
        Cor.ROXO,
        Cor.BRANCO,
        Cor.AZUL,
        Cor.AMARELO,
        Cor.LARANJA,
        Cor.PRETO,
        Cor.VERMELHO,
        Cor.VERDE
    ]
    CARTAS_POR_COR: int = 12
    TOTAL_LOCOMOTIVAS: int = 14
    
    @classmethod
    def criar_carta_normal(cls, carta_id: int, cor: Cor) -> CartaVagao:
        """
        Cria uma carta de vagão normal (não locomotiva).
        
        Args:
            carta_id: ID único da carta
            cor: Cor da carta
            
        Returns:
            CartaVagao configurada
        """
        return CartaVagao(id=carta_id, cor=cor, ehLocomotiva=False)
    
    @classmethod
    def criar_locomotiva(cls, carta_id: int) -> CartaVagao:
        """
        Cria uma carta locomotiva (coringa).
        
        Args:
            carta_id: ID único da carta
            
        Returns:
            CartaVagao locomotiva
        """
        return CartaVagao(id=carta_id, cor=Cor.LOCOMOTIVA, ehLocomotiva=True)
    
    @classmethod
    def criar_baralho_completo(cls) -> Tuple[List[CartaVagao], int]:
        """
        Cria o baralho completo de 110 cartas de vagão.
        
        Factory Method: Centraliza criação de todas as cartas.
        
        Returns:
            Tupla (lista_de_cartas, próximo_id_disponível)
            
        Composição:
        - 96 cartas normais (8 cores × 12 cartas)
        - 14 locomotivas
        - Total: 110 cartas
        """
        cartas: List[CartaVagao] = []
        contador_id = 1
        
        # Cria cartas normais (8 cores × 12 cartas = 96)
        for cor in cls.CORES_NORMAIS:
            for _ in range(cls.CARTAS_POR_COR):
                cartas.append(cls.criar_carta_normal(contador_id, cor))
                contador_id += 1
        
        # Cria locomotivas (14 cartas coringa)
        for _ in range(cls.TOTAL_LOCOMOTIVAS):
            cartas.append(cls.criar_locomotiva(contador_id))
            contador_id += 1
        
        return cartas, contador_id
