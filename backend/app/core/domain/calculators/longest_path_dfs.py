"""
Algoritmos DFS (Depth-First Search) para cálculo de maior caminho.

PADRÃO GRASP: Pure Fabrication
- Módulo auxiliar criado para algoritmos de grafos
- Separa lógica de DFS da lógica de negócio

Implementação de DFS recursivo:
- Busca em profundidade para explorar todos os caminhos possíveis
- Retorna o COMPRIMENTO total (soma de comprimentos das rotas)
- Não repete rotas (marca rotas visitadas)
- Pode revisitar cidades (apenas rotas não podem repetir)
"""

from typing import List, Set, Dict, Tuple
from app.core.domain.entities.rota import Rota


def dfs_recursivo(
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
        comprimento_restante = dfs_recursivo(
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


def dfs_com_caminho(
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
        comprimento_restante, caminho_restante = dfs_com_caminho(
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


def construir_grafo(rotas: List[Rota]) -> Dict[str, List[Tuple[str, str]]]:
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


def criar_rotas_map(rotas: List[Rota]) -> Dict[str, Rota]:
    """
    Cria mapeamento rota_id -> Rota.
    
    Args:
        rotas: Lista de rotas
        
    Returns:
        Dicionário {rota_id: Rota}
    """
    return {rota.id: rota for rota in rotas}
