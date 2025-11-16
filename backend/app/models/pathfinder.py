"""
TASK #90: Verificação de bilhetes completos (pathfinding)
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

Implementação de BFS (Breadth-First Search):
- Busca em largura para encontrar caminho entre origem e destino
- Usa fila FIFO para explorar cidades nível por nível
- Garante caminho mais curto (em número de rotas)
- Retorna True/False se existe caminho
"""

from dataclasses import dataclass, field
from typing import List, Set, Dict, Optional, Tuple
from collections import deque
from .rota import Rota
from .cidade import Cidade


@dataclass
class PathFinder:
    """
    Pure Fabrication - Classe auxiliar para busca de caminhos
    
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
        
        Algoritmo: BFS (Breadth-First Search)
        - Complexidade: O(V + E) onde V=cidades, E=rotas
        - Garante encontrar caminho se existir
        
        Args:
            origem: Cidade de origem
            destino: Cidade de destino
            rotas_conquistadas: Lista de rotas já conquistadas
            
        Returns:
            True se existe caminho, False caso contrário
            
        Exemplo:
            >>> pathfinder = PathFinder()
            >>> rotas = [rota1, rota2, rota3]  # rotas conquistadas
            >>> pathfinder.verificar_caminho_existe(
            ...     origem=PORTO_ALEGRE, 
            ...     destino=RIO_DE_JANEIRO, 
            ...     rotas_conquistadas=rotas
            ... )
            True
        """
        # Caso trivial: mesma cidade
        if origem.id == destino.id:
            return True
        
        # Caso sem rotas: impossível conectar
        if not rotas_conquistadas:
            return False
        
        # Construir grafo de adjacência a partir de rotas conquistadas
        grafo = self._construir_grafo(rotas_conquistadas)
        
        # BFS para encontrar caminho
        return self._bfs(origem.id, destino.id, grafo)
    
    def encontrar_caminho(
        self, 
        origem: Cidade, 
        destino: Cidade, 
        rotas_conquistadas: List[Rota]
    ) -> Optional[List[Cidade]]:
        """
        Encontra o caminho (lista de cidades) entre origem e destino.
        
        Retorna None se não existe caminho.
        Retorna lista de cidades representando o caminho.
        
        Args:
            origem: Cidade de origem
            destino: Cidade de destino
            rotas_conquistadas: Lista de rotas já conquistadas
            
        Returns:
            Lista de cidades no caminho, ou None se não existe
            
        Exemplo:
            >>> caminho = pathfinder.encontrar_caminho(origem, destino, rotas)
            >>> print([c.id for c in caminho])
            ['PORTO_ALEGRE', 'CURITIBA', 'SAO_PAULO', 'RIO_DE_JANEIRO']
        """
        if origem.id == destino.id:
            return [origem]
        
        if not rotas_conquistadas:
            return None
        
        grafo = self._construir_grafo(rotas_conquistadas)
        return self._bfs_com_caminho(origem.id, destino.id, grafo, rotas_conquistadas)
    
    def _construir_grafo(self, rotas: List[Rota]) -> Dict[str, List[str]]:
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
    
    def _bfs(self, origem_id: str, destino_id: str, grafo: Dict[str, List[str]]) -> bool:
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
    
    def _bfs_com_caminho(
        self, 
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
                return self._reconstruir_caminho(origem_id, destino_id, pais, rotas_conquistadas)
            
            vizinhos = grafo.get(cidade_atual, [])
            for vizinho in vizinhos:
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    pais[vizinho] = cidade_atual
                    fila.append(vizinho)
        
        return None
    
    def _reconstruir_caminho(
        self, 
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


@dataclass
class VerificadorBilhetes:
    """
    Information Expert - Verifica bilhetes completos de um jogador.
    
    Responsabilidades:
    - Verificar se jogador completou bilhete específico
    - Listar todos os bilhetes completos
    - Listar todos os bilhetes incompletos
    - Calcular pontuação de bilhetes
    
    GRASP Principles:
    - Information Expert: Conhece bilhetes e rotas do jogador
    - Low Coupling: Usa PathFinder para lógica de busca
    - High Cohesion: Focado em verificação de bilhetes
    """
    
    pathfinder: PathFinder = field(default_factory=PathFinder)
    
    def verificar_bilhete_completo(
        self, 
        bilhete, 
        rotas_conquistadas: List[Rota]
    ) -> bool:
        """
        Verifica se bilhete foi completado.
        
        Args:
            bilhete: BilheteDestino a verificar
            rotas_conquistadas: Rotas conquistadas pelo jogador
            
        Returns:
            True se existe caminho entre origem e destino
        """
        return self.pathfinder.verificar_caminho_existe(
            origem=bilhete.cidadeOrigem,
            destino=bilhete.cidadeDestino,
            rotas_conquistadas=rotas_conquistadas
        )
    
    def listar_bilhetes_completos(
        self, 
        bilhetes: List, 
        rotas_conquistadas: List[Rota]
    ) -> List:
        """
        Retorna lista de bilhetes completos.
        
        Args:
            bilhetes: Lista de BilheteDestino do jogador
            rotas_conquistadas: Rotas conquistadas pelo jogador
            
        Returns:
            Lista de bilhetes completos
        """
        completos = []
        for bilhete in bilhetes:
            if self.verificar_bilhete_completo(bilhete, rotas_conquistadas):
                completos.append(bilhete)
        return completos
    
    def listar_bilhetes_incompletos(
        self, 
        bilhetes: List, 
        rotas_conquistadas: List[Rota]
    ) -> List:
        """
        Retorna lista de bilhetes incompletos.
        
        Args:
            bilhetes: Lista de BilheteDestino do jogador
            rotas_conquistadas: Rotas conquistadas pelo jogador
            
        Returns:
            Lista de bilhetes incompletos
        """
        incompletos = []
        for bilhete in bilhetes:
            if not self.verificar_bilhete_completo(bilhete, rotas_conquistadas):
                incompletos.append(bilhete)
        return incompletos
    
    def calcular_pontuacao_bilhetes(
        self, 
        bilhetes: List, 
        rotas_conquistadas: List[Rota]
    ) -> int:
        """
        Calcula pontuação de bilhetes: +pontos para completos, -pontos para incompletos.
        
        Args:
            bilhetes: Lista de BilheteDestino do jogador
            rotas_conquistadas: Rotas conquistadas pelo jogador
            
        Returns:
            Pontuação total de bilhetes
        """
        pontuacao = 0
        
        for bilhete in bilhetes:
            if self.verificar_bilhete_completo(bilhete, rotas_conquistadas):
                pontuacao += bilhete.pontos
            else:
                pontuacao -= bilhete.pontos
        
        return pontuacao
