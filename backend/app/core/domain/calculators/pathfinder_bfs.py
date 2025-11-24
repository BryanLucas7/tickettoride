"""
Algoritmos BFS (Breadth-First Search) para pathfinding.

PADRÃO GRASP: Pure Fabrication
- Módulo auxiliar criado para algoritmos de grafos
- Separa lógica de BFS da lógica de negócio

Implementação de BFS:
- Busca em largura para encontrar caminho entre origem e destino
- Usa fila FIFO para explorar cidades nível por nível
- Garante caminho mais curto (em número de rotas)
"""

from typing import List, Set, Dict, Optional
from collections import deque
from app.core.domain.entities.rota import Rota
from app.core.domain.entities.cidade import Cidade


def construir_grafo(rotas: List[Rota]) -> Dict[str, List[str]]:
    """
    Constrói grafo de adjacência a partir de rotas.
    
    Grafo não-direcionado: se A->B existe, então B->A também existe.
    
    Args:
        rotas: Lista de rotas conquistadas
        
    Returns:
        Dicionário {cidade_id: [cidade_vizinha_id, ...]}
    """
    grafo: Dict[str, List[str]] = {}
    
    for rota in rotas:
        cidade_a_id = rota.cidadeA.id
        cidade_b_id = rota.cidadeB.id
        
        # Adicionar conexão A -> B
        if cidade_a_id not in grafo:
            grafo[cidade_a_id] = []
        grafo[cidade_a_id].append(cidade_b_id)
        
        # Adicionar conexão B -> A (grafo não-direcionado)
        if cidade_b_id not in grafo:
            grafo[cidade_b_id] = []
        grafo[cidade_b_id].append(cidade_a_id)
    
    return grafo


def bfs(origem_id: str, destino_id: str, grafo: Dict[str, List[str]]) -> bool:
    """
    BFS (Breadth-First Search) para verificar conectividade.
    
    Algoritmo:
    1. Iniciar fila com origem
    2. Marcar origem como visitada
    3. Enquanto fila não vazia:
       - Remover cidade da fila
       - Se cidade == destino: retornar True
       - Para cada vizinho não visitado:
         - Marcar como visitado
         - Adicionar à fila
    4. Se fila esvaziar sem encontrar: retornar False
    
    Args:
        origem_id: ID da cidade de origem
        destino_id: ID da cidade de destino
        grafo: Grafo de adjacência
        
    Returns:
        True se existe caminho, False caso contrário
    """
    # Verificar se origem existe no grafo
    if origem_id not in grafo:
        return False
    
    # Inicializar BFS
    fila = deque([origem_id])
    visitados: Set[str] = {origem_id}
    
    while fila:
        cidade_atual = fila.popleft()
        
        # Encontrou destino!
        if cidade_atual == destino_id:
            return True
        
        # Explorar vizinhos
        vizinhos = grafo.get(cidade_atual, [])
        for vizinho in vizinhos:
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append(vizinho)
    
    # Não encontrou caminho
    return False


def bfs_com_caminho(
    origem_id: str, 
    destino_id: str, 
    grafo: Dict[str, List[str]],
    rotas_conquistadas: List[Rota]
) -> Optional[List[Cidade]]:
    """
    BFS que rastreia o caminho percorrido.
    
    Mantém dicionário de pais para reconstruir caminho ao final.
    
    Args:
        origem_id: ID da cidade de origem
        destino_id: ID da cidade de destino
        grafo: Grafo de adjacência
        rotas_conquistadas: Rotas para obter objetos Cidade
        
    Returns:
        Lista de cidades no caminho, ou None se não existe
    """
    if origem_id not in grafo:
        return None
    
    # Inicializar BFS com rastreamento de pais
    fila = deque([origem_id])
    visitados: Set[str] = {origem_id}
    pais: Dict[str, Optional[str]] = {origem_id: None}
    
    while fila:
        cidade_atual = fila.popleft()
        
        if cidade_atual == destino_id:
            # Reconstruir caminho dos pais
            return reconstruir_caminho(origem_id, destino_id, pais, rotas_conquistadas)
        
        vizinhos = grafo.get(cidade_atual, [])
        for vizinho in vizinhos:
            if vizinho not in visitados:
                visitados.add(vizinho)
                pais[vizinho] = cidade_atual
                fila.append(vizinho)
    
    return None


def reconstruir_caminho(
    origem_id: str, 
    destino_id: str, 
    pais: Dict[str, Optional[str]],
    rotas_conquistadas: List[Rota]
) -> List[Cidade]:
    """
    Reconstrói caminho a partir do dicionário de pais.
    
    Percorre do destino até a origem usando pais[cidade].
    Inverte lista ao final para obter origem → destino.
    
    Args:
        origem_id: ID da origem
        destino_id: ID do destino
        pais: Dicionário de pais {cidade: pai}
        rotas_conquistadas: Rotas para obter objetos Cidade
        
    Returns:
        Lista de objetos Cidade no caminho
    """
    # Criar mapa id -> Cidade
    cidades_map: Dict[str, Cidade] = {}
    for rota in rotas_conquistadas:
        cidades_map[rota.cidadeA.id] = rota.cidadeA
        cidades_map[rota.cidadeB.id] = rota.cidadeB
    
    # Reconstruir caminho do destino até a origem
    caminho_ids: List[str] = []
    cidade_atual = destino_id
    
    while cidade_atual is not None:
        caminho_ids.append(cidade_atual)
        cidade_atual = pais.get(cidade_atual)
    
    # Inverter para obter origem → destino
    caminho_ids.reverse()
    
    # Converter IDs para objetos Cidade
    caminho_cidades = [cidades_map[cidade_id] for cidade_id in caminho_ids]
    
    return caminho_cidades
