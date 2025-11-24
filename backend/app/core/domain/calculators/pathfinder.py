"""
ATENÇÃO: Este arquivo foi refatorado para melhor manutenibilidade.
As implementações foram movidas para módulos separados:
- pathfinder_bfs.py: Algoritmos BFS
===========================================================

PADRÃO GRASP: Pure Fabrication
- PathFinder não representa conceito do domínio real
- Criado para responsabilidade específica de busca de caminhos
- Aplica algoritmos de grafos (BFS) para verificação de conectividade

PADRÃO GRASP: Information Expert
- Tabuleiro conhece rotas → PathFinder consulta Tabuleiro
- Jogador conhece rotas conquistadas → PathFinder recebe lista filtrada

PADRÃO GRASP: Low Coupling
- PathFinder não depende de Jogador diretamente
- Recebe apenas dados necessários (lista de rotas)
"""

from dataclasses import dataclass
from typing import List, Optional, Dict
from app.core.domain.entities.rota import Rota
from app.core.domain.entities.cidade import Cidade
from .pathfinder_bfs import (
    construir_grafo,
    bfs,
    bfs_com_caminho
)


@dataclass
class PathFinder:
    """
    Pure Fabrication - Classe auxiliar para busca de caminhos.
    
    Responsabilidades:
    - Verificar se existe caminho entre duas cidades
    - Calcular caminho usando apenas rotas conquistadas
    - Aplicar BFS para encontrar conectividade
    
    GRASP Principles:
    - Pure Fabrication: Não representa conceito do domínio
    - Low Coupling: Recebe apenas rotas como dependência
    - High Cohesion: Focado apenas em pathfinding
    """
    
    def verificar_caminho_existe(
        self, 
        origem: Cidade, 
        destino: Cidade, 
        rotas_conquistadas: List[Rota]
    ) -> bool:
        """
        Verifica se existe caminho entre origem e destino
        usando apenas rotas conquistadas pelo jogador.
        """
        if origem.id == destino.id:
            return True
        
        if not rotas_conquistadas:
            return False
        
        grafo = construir_grafo(rotas_conquistadas)
        return bfs(origem.id, destino.id, grafo)
    
    def encontrar_caminho(
        self, 
        origem: Cidade, 
        destino: Cidade, 
        rotas_conquistadas: List[Rota]
    ) -> Optional[List[Cidade]]:
        """
        Encontra o caminho (lista de cidades) entre origem e destino.
        """
        if origem.id == destino.id:
            return [origem]
        
        if not rotas_conquistadas:
            return None
        
        grafo = construir_grafo(rotas_conquistadas)
        return bfs_com_caminho(origem.id, destino.id, grafo, rotas_conquistadas)
    
    # Métodos privados agora delegam para funções do módulo BFS
    def _construir_grafo(self, rotas: List[Rota]) -> Dict[str, List[str]]:
        return construir_grafo(rotas)
    
    def _bfs(self, origem_id: str, destino_id: str, grafo: Dict[str, List[str]]) -> bool:
        return bfs(origem_id, destino_id, grafo)
    
    def _bfs_com_caminho(self, origem_id: str, destino_id: str, 
                         grafo: Dict[str, List[str]], rotas_conquistadas: List[Rota]) -> Optional[List[Cidade]]:
        return bfs_com_caminho(origem_id, destino_id, grafo, rotas_conquistadas)


__all__ = ['PathFinder']
