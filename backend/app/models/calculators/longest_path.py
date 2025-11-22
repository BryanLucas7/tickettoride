"""
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

Implementação de DFS (Depth-First Search) recursivo:
- Busca em profundidade para explorar todos os caminhos possíveis
- Retorna o COMPRIMENTO total (soma de comprimentos das rotas)
- Não repete rotas (marca rotas visitadas)
- Pode revisitar cidades (apenas rotas não podem repetir)
- Retorna tamanho do maior caminho encontrado

Regras Ticket to Ride:
- Maior Caminho Contínuo = sequência de rotas sem repetir
- Pontuação: jogador com maior caminho ganha +10 pontos no fim
- Pode passar pela mesma cidade múltiplas vezes
- Conta o COMPRIMENTO das rotas (não quantidade de rotas)
"""

from dataclasses import dataclass, field
from typing import List, Set, Dict, Tuple
from ..entities.rota import Rota
from ..entities.cidade import Cidade


@dataclass
class LongestPathCalculator:
    """
    Pure Fabrication - Classe auxiliar para cálculo de maior caminho
    
    Responsabilidades:
    - Calcular maior caminho contínuo de rotas
    - Encontrar sequência mais longa sem repetir rotas
    - Aplicar DFS recursivo para exploração exaustiva
    
    GRASP Principles:
    - Pure Fabrication: Não representa conceito do domínio
    - Low Coupling: Recebe apenas rotas como dependência
    - High Cohesion: Focado apenas em cálculo de caminho
    
    Algoritmo:
    - DFS recursivo partindo de cada cidade
    - Marca rotas visitadas para evitar repetição
    - Calcula soma de comprimentos das rotas
    - Retorna maior comprimento encontrado
    """
    
    def calcular_maior_caminho(self, rotas_conquistadas: List[Rota]) -> int:
        """
        Calcula o comprimento do maior caminho contínuo.
        
        Algoritmo:
        1. Tenta começar de cada cidade possível
        2. Para cada partida, faz DFS recursivo
        3. Retorna o maior comprimento encontrado
        
        Complexidade: O(n! * n) onde n = número de rotas
        - Explora todas as permutações possíveis de rotas
        - Para grafos pequenos (< 50 rotas), é aceitável
        
        Args:
            rotas_conquistadas: Lista de rotas já conquistadas pelo jogador
            
        Returns:
            Comprimento do maior caminho (soma de comprimentos das rotas)
            
        Exemplo:
            >>> calculator = LongestPathCalculator()
            >>> rotas = [rota1, rota2, rota3]  # rotas conquistadas
            >>> comprimento = calculator.calcular_maior_caminho(rotas)
            >>> print(comprimento)  # Ex: 15 (soma dos comprimentos)
            15
        """
        if not rotas_conquistadas:
            return 0
        
        # Construir grafo de adjacência
        grafo = self._construir_grafo(rotas_conquistadas)
        
        # Testar DFS começando de cada cidade
        maior_comprimento = 0
        
        for cidade_id in grafo.keys():
            # DFS recursivo partindo desta cidade
            visitadas: Set[str] = set()
            comprimento = self._dfs_recursivo(
                cidade_atual=cidade_id,
                grafo=grafo,
                rotas_visitadas=visitadas,
                rotas_map=self._criar_rotas_map(rotas_conquistadas)
            )
            
            maior_comprimento = max(maior_comprimento, comprimento)
        
        return maior_comprimento
    
    def encontrar_maior_caminho(self, rotas_conquistadas: List[Rota]) -> Tuple[int, List[Rota]]:
        """
        Encontra o maior caminho E retorna a lista de rotas.
        
        Args:
            rotas_conquistadas: Lista de rotas já conquistadas
            
        Returns:
            Tupla (comprimento, lista_de_rotas)
            
        Exemplo:
            >>> comprimento, caminho = calculator.encontrar_maior_caminho(rotas)
            >>> print(f"Comprimento: {comprimento}, Rotas: {len(caminho)}")
            Comprimento: 15, Rotas: 4
        """
        if not rotas_conquistadas:
            return (0, [])
        
        grafo = self._construir_grafo(rotas_conquistadas)
        rotas_map = self._criar_rotas_map(rotas_conquistadas)
        
        melhor_comprimento = 0
        melhor_caminho: List[Rota] = []
        
        for cidade_id in grafo.keys():
            visitadas: Set[str] = set()
            caminho_atual: List[str] = []
            
            comprimento, caminho = self._dfs_com_caminho(
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
    
    def _construir_grafo(self, rotas: List[Rota]) -> Dict[str, List[Tuple[str, str]]]:
        """
        Constrói grafo de adjacência com informação de rota.
        
        Estrutura: {cidade_id: [(cidade_vizinha_id, rota_id), ...]}
        
        Args:
            rotas: Lista de rotas conquistadas
            
        Returns:
            Dicionário representando grafo
        """
        grafo: Dict[str, List[Tuple[str, str]]] = {}
        
        for rota in rotas:
            cidade_a_id = rota.cidadeA.id
            cidade_b_id = rota.cidadeB.id
            rota_id = rota.id
            
            # Adicionar A -> B
            if cidade_a_id not in grafo:
                grafo[cidade_a_id] = []
            grafo[cidade_a_id].append((cidade_b_id, rota_id))
            
            # Adicionar B -> A (grafo não-direcionado)
            if cidade_b_id not in grafo:
                grafo[cidade_b_id] = []
            grafo[cidade_b_id].append((cidade_a_id, rota_id))
        
        return grafo
    
    def _criar_rotas_map(self, rotas: List[Rota]) -> Dict[str, Rota]:
        """
        Cria mapeamento rota_id -> Rota.
        
        Args:
            rotas: Lista de rotas
            
        Returns:
            Dicionário {rota_id: Rota}
        """
        return {rota.id: rota for rota in rotas}
    
    def _dfs_recursivo(
        self,
        cidade_atual: str,
        grafo: Dict[str, List[Tuple[str, str]]],
        rotas_visitadas: Set[str],
        rotas_map: Dict[str, Rota]
    ) -> int:
        """
        DFS recursivo para calcular maior caminho.
        
        Algoritmo:
        1. Explorar cada vizinho não visitado
        2. Marcar rota como visitada
        3. Recursão: calcular comprimento + DFS no vizinho
        4. Desmarcar rota (backtracking)
        5. Retornar maior comprimento encontrado
        
        Args:
            cidade_atual: ID da cidade atual
            grafo: Grafo de adjacência
            rotas_visitadas: Set de IDs de rotas já visitadas
            rotas_map: Mapa rota_id -> Rota
            
        Returns:
            Comprimento do maior caminho partindo desta cidade
        """
        maior_comprimento = 0
        
        # Explorar todos os vizinhos
        vizinhos = grafo.get(cidade_atual, [])
        
        for cidade_vizinha, rota_id in vizinhos:
            # Se rota já foi visitada, skip
            if rota_id in rotas_visitadas:
                continue
            
            # Marcar rota como visitada
            rotas_visitadas.add(rota_id)
            
            # Obter comprimento desta rota
            comprimento_rota = rotas_map[rota_id].comprimento
            
            # Recursão: explorar a partir do vizinho
            comprimento_restante = self._dfs_recursivo(
                cidade_atual=cidade_vizinha,
                grafo=grafo,
                rotas_visitadas=rotas_visitadas,
                rotas_map=rotas_map
            )
            
            # Calcular comprimento total deste caminho
            comprimento_total = comprimento_rota + comprimento_restante
            
            # Atualizar maior comprimento
            maior_comprimento = max(maior_comprimento, comprimento_total)
            
            # Backtracking: desmarcar rota para explorar outros caminhos
            rotas_visitadas.remove(rota_id)
        
        return maior_comprimento
    
    def _dfs_com_caminho(
        self,
        cidade_atual: str,
        grafo: Dict[str, List[Tuple[str, str]]],
        rotas_visitadas: Set[str],
        caminho_atual: List[str],
        rotas_map: Dict[str, Rota]
    ) -> Tuple[int, List[str]]:
        """
        DFS recursivo que rastreia o caminho percorrido.
        
        Args:
            cidade_atual: ID da cidade atual
            grafo: Grafo de adjacência
            rotas_visitadas: Set de rotas visitadas
            caminho_atual: Lista de IDs de rotas no caminho
            rotas_map: Mapa rota_id -> Rota
            
        Returns:
            Tupla (comprimento, lista_de_rota_ids)
        """
        melhor_comprimento = 0
        melhor_caminho = caminho_atual.copy()
        
        vizinhos = grafo.get(cidade_atual, [])
        
        for cidade_vizinha, rota_id in vizinhos:
            if rota_id in rotas_visitadas:
                continue
            
            # Marcar e adicionar ao caminho
            rotas_visitadas.add(rota_id)
            caminho_atual.append(rota_id)
            
            comprimento_rota = rotas_map[rota_id].comprimento
            
            # Recursão
            comprimento_restante, caminho_restante = self._dfs_com_caminho(
                cidade_atual=cidade_vizinha,
                grafo=grafo,
                rotas_visitadas=rotas_visitadas,
                caminho_atual=caminho_atual,
                rotas_map=rotas_map
            )
            
            comprimento_total = comprimento_rota + comprimento_restante
            
            # Atualizar melhor
            if comprimento_total > melhor_comprimento:
                melhor_comprimento = comprimento_total
                melhor_caminho = caminho_restante.copy()
            
            # Backtracking
            rotas_visitadas.remove(rota_id)
            caminho_atual.pop()
        
        return (melhor_comprimento, melhor_caminho)
