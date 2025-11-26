"""
CartaConverter - Conversor de cores para objetos CartaVagao.

Padrão GRASP: Pure Fabrication
- Extraído de RouteConquestService para responsabilidade única
- Converte strings de cores em objetos CartaVagao da mão do jogador

Responsabilidades:
- Buscar cartas na mão do jogador por cor
- Validar se cartas existem
- Retornar lista de CartaVagao correspondente
"""

from typing import List, Tuple, Optional
from ..core.domain.entities.carta_vagao import CartaVagao
from ..core.domain.entities.jogador import Jogador


class CartaConversionError(Exception):
    """Exceção para erros de conversão de cartas."""
    pass


class CartaConverter:
    """
    Conversor de strings de cores para objetos CartaVagao.
    
    Responsável por buscar cartas na mão do jogador baseado nas cores
    informadas, sem remover da mão (apenas identificar).
    """
    
    @staticmethod
    def converter_cores_para_cartas(
        jogador: Jogador,
        cartas_cores: List[str]
    ) -> Tuple[List[CartaVagao], Optional[str]]:
        """
        Converte lista de cores em lista de CartaVagao da mão do jogador.
        
        Busca cartas correspondentes na mão do jogador sem removê-las.
        O controller que usar as cartas é responsável por removê-las depois.
        
        Args:
            jogador: Jogador cuja mão será consultada
            cartas_cores: Lista de strings de cores (ex: ["azul", "vermelho", "locomotiva"])
            
        Returns:
            Tupla (cartas_encontradas, erro):
            - cartas_encontradas: Lista de CartaVagao se sucesso, lista vazia se erro
            - erro: Mensagem de erro se falhar, None se sucesso
            
        Example:
            >>> cartas, erro = CartaConverter.converter_cores_para_cartas(
            ...     jogador, ["azul", "azul", "locomotiva"]
            ... )
            >>> if erro:
            ...     print(f"Erro: {erro}")
            >>> else:
            ...     print(f"Encontradas {len(cartas)} cartas")
        """
        cartas_usadas: List[CartaVagao] = []
        cartas_disponiveis = list(jogador.mao.cartasVagao)  # Cópia para busca
        
        for cor_str in cartas_cores:
            carta_encontrada = CartaConverter._buscar_carta_por_cor(
                cor_str, cartas_disponiveis
            )
            
            if not carta_encontrada:
                return [], f"Carta {cor_str} não encontrada na mão do jogador"
            
            cartas_usadas.append(carta_encontrada)
        
        return cartas_usadas, None
    
    @staticmethod
    def _buscar_carta_por_cor(
        cor_str: str,
        cartas_disponiveis: List[CartaVagao]
    ) -> Optional[CartaVagao]:
        """
        Busca uma carta pela cor na lista de cartas disponíveis.
        
        Remove a carta encontrada da lista de disponíveis para evitar
        selecionar a mesma carta duas vezes.
        
        Args:
            cor_str: String da cor a buscar
            cartas_disponiveis: Lista de cartas disponíveis (será modificada)
            
        Returns:
            CartaVagao encontrada ou None
        """
        for i, carta in enumerate(cartas_disponiveis):
            if CartaConverter._carta_corresponde_cor(carta, cor_str):
                # Remove da lista de busca para não pegar duplicada
                cartas_disponiveis.pop(i)
                return carta
        return None
    
    @staticmethod
    def _carta_corresponde_cor(carta: CartaVagao, cor_str: str) -> bool:
        """
        Verifica se a carta corresponde à cor informada.
        
        Args:
            carta: CartaVagao a verificar
            cor_str: String da cor
            
        Returns:
            True se corresponde, False caso contrário
        """
        if cor_str == "locomotiva" and carta.ehLocomotiva:
            return True
        return carta.cor.value == cor_str
