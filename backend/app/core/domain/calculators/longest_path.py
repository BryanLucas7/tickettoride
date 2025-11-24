"""
ATENÇÃO: Este arquivo foi refatorado para melhor manutenibilidade.
As implementações foram movidas para módulos separados:
- longest_path_dfs.py: Algoritmos DFS
============================================

PADRÃO GRASP: Pure Fabrication
- LongestPathCalculator não representa conceito do domínio real
- Criado para responsabilidade específica de cálculo de maior caminho
- Aplica algoritmos de grafos (DFS recursivo) para calcular comprimento

PADRÃO GRASP: Information Expert
- Tabuleiro conhece rotas → LongestPathCalculator consulta rotas
- Jogador conhece rotas conquistadas → passa lista de rotas

PADRÃO GRASP: Low Coupling
- LongestPathCalculator não depende de Jogador diretamente
- Recebe apenas dados necessários (lista de rotas)
"""

from dataclasses import dataclass
from typing import List, Set, Tuple, Dict
from app.core.domain.entities.rota import Rota
from .longest_path_dfs import (
    dfs_recursivo,
    dfs_com_caminho,
    construir_grafo,
    criar_rotas_map
)


@dataclass
class LongestPathCalculator:
    """
    Pure Fabrication - Classe auxiliar para cálculo de maior caminho.
    
    Responsabilidades:
    - Calcular maior caminho contínuo de rotas
    - Encontrar sequência mais longa sem repetir rotas
    - Aplicar DFS recursivo para exploração exaustiva
    
    GRASP Principles:
    - Pure Fabrication: Não representa conceito do domínio
    - Low Coupling: Recebe apenas rotas como dependência
    - High Cohesion: Focado apenas em cálculo de caminho
    """
    
    def calcular_maior_caminho(self, rotas_conquistadas: List[Rota]) -> int:
        """Calcula o comprimento do maior caminho contínuo."""
        if not rotas_conquistadas:
            return 0
        
        grafo = construir_grafo(rotas_conquistadas)
        rotas_map = criar_rotas_map(rotas_conquistadas)
        maior_comprimento = 0
        
        for cidade_id in grafo.keys():
            visitadas: Set[str] = set()
            comprimento = dfs_recursivo(
                cidade_atual=cidade_id,
                grafo=grafo,
                rotas_visitadas=visitadas,
                rotas_map=rotas_map
            )
            maior_comprimento = max(maior_comprimento, comprimento)
        
        return maior_comprimento
    
    def encontrar_maior_caminho(self, rotas_conquistadas: List[Rota]) -> Tuple[int, List[Rota]]:
        """Encontra o maior caminho E retorna a lista de rotas."""
        if not rotas_conquistadas:
            return (0, [])
        
        grafo = construir_grafo(rotas_conquistadas)
        rotas_map = criar_rotas_map(rotas_conquistadas)
        melhor_comprimento = 0
        melhor_caminho: List[Rota] = []
        
        for cidade_id in grafo.keys():
            visitadas: Set[str] = set()
            caminho_atual: List[str] = []
            
            comprimento, caminho = dfs_com_caminho(
                cidade_atual=cidade_id,
                grafo=grafo,
                rotas_visitadas=visitadas,
                caminho_atual=caminho_atual,
                rotas_map=rotas_map
            )
            
            if comprimento > melhor_comprimento:
                melhor_comprimento = comprimento
                melhor_caminho = [rotas_map[rota_id] for rota_id in caminho]
        
        return (melhor_comprimento, melhor_caminho)
    
    # Métodos privados agora delegam para funções do módulo DFS
    def _construir_grafo(self, rotas: List[Rota]) -> Dict[str, List[Tuple[str, str]]]:
        return construir_grafo(rotas)
    
    def _criar_rotas_map(self, rotas: List[Rota]) -> Dict[str, Rota]:
        return criar_rotas_map(rotas)
    
    def _dfs_recursivo(self, cidade_atual: str, grafo: Dict[str, List[Tuple[str, str]]], 
                       rotas_visitadas: Set[str], rotas_map: Dict[str, Rota]) -> int:
        return dfs_recursivo(cidade_atual, grafo, rotas_visitadas, rotas_map)
    
    def _dfs_com_caminho(self, cidade_atual: str, grafo: Dict[str, List[Tuple[str, str]]], 
                         rotas_visitadas: Set[str], caminho_atual: List[str], 
                         rotas_map: Dict[str, Rota]) -> Tuple[int, List[str]]:
        return dfs_com_caminho(cidade_atual, grafo, rotas_visitadas, caminho_atual, rotas_map)


__all__ = ['LongestPathCalculator']
