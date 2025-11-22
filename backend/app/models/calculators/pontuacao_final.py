"""

PADRÃO GRASP: Information Expert
- PontuacaoFinalCalculator conhece regras de pontuação → calcula pontos
- Utiliza componentes especializados (VerificadorBilhetes, LongestPathCalculator)
- Centraliza lógica de pontuação final

PADRÃO GRASP: Controller
- PontuacaoFinalService coordena cálculo de pontuação final
- Orquestra componentes: bilhetes, rotas, maior caminho
- Determina vencedor e aplica critérios de desempate

PADRÃO GRASP: Low Coupling
- PontuacaoFinalCalculator usa interfaces de outros componentes
- Não depende de implementações específicas

Regras Ticket to Ride - Pontuação Final:
1. Pontos de rotas conquistadas (já calculados durante jogo)
2. +pontos para bilhetes completos
3. -pontos para bilhetes incompletos
4. +10 pontos para jogador(es) com maior caminho contínuo

Critérios de Desempate (em ordem):
1. Mais bilhetes completos
2. Maior caminho contínuo (comprimento)
3. Empate permanece
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from .pathfinder import PathFinder
from .longest_path import LongestPathCalculator
from ..entities.rota import Rota
from ..entities.bilhete_destino import BilheteDestino


@dataclass
class ResultadoJogador:
    """
    Resultado final de um jogador.
    
    Atributos:
        jogador_id: ID do jogador
        pontos_rotas: Pontos de rotas conquistadas
        pontos_bilhetes_completos: Pontos de bilhetes completos
        pontos_bilhetes_incompletos: Pontos perdidos de bilhetes incompletos (negativo)
        bonus_maior_caminho: +10 se tem maior caminho, 0 caso contrário
        pontuacao_total: Soma de todos os pontos
        bilhetes_completos: Quantidade de bilhetes completos
        bilhetes_incompletos: Quantidade de bilhetes incompletos
        comprimento_maior_caminho: Comprimento do maior caminho contínuo
        bilhetes_completos_lista: Referência aos objetos de bilhetes completos
        bilhetes_incompletos_lista: Referência aos objetos de bilhetes incompletos
    """
    jogador_id: str
    pontos_rotas: int = 0
    pontos_bilhetes_completos: int = 0
    pontos_bilhetes_incompletos: int = 0
    bonus_maior_caminho: int = 0
    pontuacao_total: int = 0
    bilhetes_completos: int = 0
    bilhetes_incompletos: int = 0
    comprimento_maior_caminho: int = 0
    bilhetes_completos_lista: List[BilheteDestino] = field(default_factory=list)
    bilhetes_incompletos_lista: List[BilheteDestino] = field(default_factory=list)
    
    def __post_init__(self):
        """Calcula pontuação total automaticamente"""
        self.pontuacao_total = (
            self.pontos_rotas + 
            self.pontos_bilhetes_completos + 
            self.pontos_bilhetes_incompletos +  # já é negativo
            self.bonus_maior_caminho
        )


@dataclass
class ResultadoFinal:
    """
    Resultado final do jogo.
    
    Atributos:
        resultados: Dicionário {jogador_id: ResultadoJogador}
        vencedor: ID do jogador vencedor (ou lista se empate)
        jogadores_com_maior_caminho: Lista de IDs com maior caminho (+10 pts)
        ranking: Lista de jogador_ids ordenados por pontuação
    """
    resultados: Dict[str, ResultadoJogador]
    vencedor: str | List[str]
    jogadores_com_maior_caminho: List[str]
    ranking: List[str]


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


@dataclass
class PontuacaoFinalCalculator:
    """
    Information Expert - Calcula pontuação final completa.
    
    Responsabilidades:
    - Calcular pontuação de cada jogador
    - Aplicar bônus de maior caminho
    - Determinar vencedor com critérios de desempate
    
    GRASP Principles:
    - Information Expert: Conhece regras de pontuação
    - Low Coupling: Usa componentes especializados
    - High Cohesion: Focado em pontuação final
    """
    
    verificador_bilhetes: VerificadorBilhetes = field(default_factory=VerificadorBilhetes)
    longest_path_calculator: LongestPathCalculator = field(default_factory=LongestPathCalculator)
    
    def calcular_pontuacao_jogador(
        self,
        jogador_id: str,
        pontos_rotas: int,
        bilhetes: List[BilheteDestino],
        rotas_conquistadas: List[Rota],
        tem_maior_caminho: bool = False
    ) -> ResultadoJogador:
        """
        Calcula pontuação final de um jogador.
        
        Args:
            jogador_id: ID do jogador
            pontos_rotas: Pontos já acumulados de rotas durante o jogo
            bilhetes: Lista de bilhetes do jogador
            rotas_conquistadas: Lista de rotas conquistadas pelo jogador
            tem_maior_caminho: Se jogador tem maior caminho (+10 pts)
            
        Returns:
            ResultadoJogador com pontuação detalhada
        """
        # Calcular bilhetes completos e incompletos
        bilhetes_completos = self.verificador_bilhetes.listar_bilhetes_completos(
            bilhetes=bilhetes,
            rotas_conquistadas=rotas_conquistadas
        )
        
        bilhetes_incompletos = self.verificador_bilhetes.listar_bilhetes_incompletos(
            bilhetes=bilhetes,
            rotas_conquistadas=rotas_conquistadas
        )
        
        # Calcular pontos de bilhetes
        pontos_completos = sum(b.pontos for b in bilhetes_completos)
        pontos_incompletos = -sum(b.pontos for b in bilhetes_incompletos)  # negativo
        
        # Calcular maior caminho
        comprimento_caminho = self.longest_path_calculator.calcular_maior_caminho(rotas_conquistadas)
        
        # Bônus de maior caminho
        bonus = 10 if tem_maior_caminho else 0
        
        return ResultadoJogador(
            jogador_id=jogador_id,
            pontos_rotas=pontos_rotas,
            pontos_bilhetes_completos=pontos_completos,
            pontos_bilhetes_incompletos=pontos_incompletos,
            bonus_maior_caminho=bonus,
            bilhetes_completos=len(bilhetes_completos),
            bilhetes_incompletos=len(bilhetes_incompletos),
            comprimento_maior_caminho=comprimento_caminho,
            bilhetes_completos_lista=bilhetes_completos,
            bilhetes_incompletos_lista=bilhetes_incompletos
        )
    
    def determinar_vencedor(
        self,
        resultados: Dict[str, ResultadoJogador]
    ) -> str | List[str]:
        """
        Determina vencedor com critérios de desempate.
        
        Critérios (em ordem):
        1. Maior pontuação total
        2. Mais bilhetes completos
        3. Maior caminho contínuo (comprimento)
        4. Empate permanece
        
        Args:
            resultados: Dicionário {jogador_id: ResultadoJogador}
            
        Returns:
            ID do vencedor ou lista de IDs se empate
        """
        if not resultados:
            return []
        
        # Ordenar por critérios
        jogadores_ordenados = sorted(
            resultados.items(),
            key=lambda x: (
                x[1].pontuacao_total,
                x[1].bilhetes_completos,
                x[1].comprimento_maior_caminho
            ),
            reverse=True
        )
        
        # Pegar primeiro (maior pontuação)
        vencedor_id, vencedor_resultado = jogadores_ordenados[0]
        
        # Verificar empates
        empatados = [vencedor_id]
        
        for jogador_id, resultado in jogadores_ordenados[1:]:
            # Empate total (mesmos critérios)
            if (
                resultado.pontuacao_total == vencedor_resultado.pontuacao_total and
                resultado.bilhetes_completos == vencedor_resultado.bilhetes_completos and
                resultado.comprimento_maior_caminho == vencedor_resultado.comprimento_maior_caminho
            ):
                empatados.append(jogador_id)
            else:
                break  # Não empata mais
        
        # Retornar único ou lista
        if len(empatados) == 1:
            return empatados[0]
        else:
            return empatados


@dataclass
class PontuacaoFinalService:
    """
    Controller - Coordena cálculo de pontuação final.
    
    Responsabilidades:
    - Orquestrar cálculo de pontuação de todos os jogadores
    - Determinar jogadores com maior caminho
    - Aplicar bônus de maior caminho
    - Determinar vencedor final
    - Gerar ranking
    
    GRASP Principles:
    - Controller: Coordena fluxo de pontuação final
    - Low Coupling: Delega cálculos ao PontuacaoFinalCalculator
    - High Cohesion: Focado em coordenação de pontuação
    """
    
    calculator: PontuacaoFinalCalculator = field(default_factory=PontuacaoFinalCalculator)
    
    def calcular_resultado_final(
        self,
        jogadores_dados: Dict[str, Dict]
    ) -> ResultadoFinal:
        """
        Calcula resultado final do jogo.
        
        Args:
            jogadores_dados: Dicionário {
                jogador_id: {
                    'pontos_rotas': int,
                    'bilhetes': List[BilheteDestino],
                    'rotas_conquistadas': List[Rota]
                }
            }
            
        Returns:
            ResultadoFinal com todos os resultados
            
        Exemplo:
            >>> service = PontuacaoFinalService()
            >>> dados = {
            ...     'alice': {
            ...         'pontos_rotas': 30,
            ...         'bilhetes': [bilhete1, bilhete2],
            ...         'rotas_conquistadas': [rota1, rota2, rota3]
            ...     },
            ...     'bob': {
            ...         'pontos_rotas': 25,
            ...         'bilhetes': [bilhete3],
            ...         'rotas_conquistadas': [rota4, rota5]
            ...     }
            ... }
            >>> resultado = service.calcular_resultado_final(dados)
            >>> print(resultado.vencedor)
            'alice'
        """
        # 1. Determinar jogadores com maior caminho
        jogadores_rotas = {
            jogador_id: dados['rotas_conquistadas']
            for jogador_id, dados in jogadores_dados.items()
        }
        
        jogadores_com_maior = self._determinar_jogadores_maior_caminho(jogadores_rotas)
        
        # 2. Calcular pontuação de cada jogador
        resultados: Dict[str, ResultadoJogador] = {}
        
        for jogador_id, dados in jogadores_dados.items():
            tem_maior = jogador_id in jogadores_com_maior
            
            resultado = self.calculator.calcular_pontuacao_jogador(
                jogador_id=jogador_id,
                pontos_rotas=dados['pontos_rotas'],
                bilhetes=dados['bilhetes'],
                rotas_conquistadas=dados['rotas_conquistadas'],
                tem_maior_caminho=tem_maior
            )
            
            resultados[jogador_id] = resultado
        
        # 3. Determinar vencedor
        vencedor = self.calculator.determinar_vencedor(resultados)
        
        # 4. Gerar ranking
        ranking = self._gerar_ranking(resultados)
        
        return ResultadoFinal(
            resultados=resultados,
            vencedor=vencedor,
            jogadores_com_maior_caminho=jogadores_com_maior,
            ranking=ranking
        )
    
    def _determinar_jogadores_maior_caminho(
        self,
        jogadores_rotas: Dict[str, List[Rota]]
    ) -> List[str]:
        """
        Determina quais jogadores têm o maior caminho contínuo.
        
        Args:
            jogadores_rotas: {jogador_id: rotas_conquistadas}
            
        Returns:
            Lista de IDs de jogadores com maior caminho
        """
        if not jogadores_rotas:
            return []
        
        # Calcular comprimento para cada jogador
        comprimentos: Dict[str, int] = {}
        
        for jogador_id, rotas in jogadores_rotas.items():
            comprimento = self.calculator.longest_path_calculator.calcular_maior_caminho(rotas)
            comprimentos[jogador_id] = comprimento
        
        # Encontrar maior
        maior = max(comprimentos.values())
        
        # Retornar todos com maior
        return [
            jogador_id
            for jogador_id, comprimento in comprimentos.items()
            if comprimento == maior
        ]
    
    def _gerar_ranking(
        self,
        resultados: Dict[str, ResultadoJogador]
    ) -> List[str]:
        """
        Gera ranking de jogadores ordenado por pontuação.
        
        Args:
            resultados: {jogador_id: ResultadoJogador}
            
        Returns:
            Lista de jogador_ids ordenados (primeiro = vencedor)
        """
        jogadores_ordenados = sorted(
            resultados.items(),
            key=lambda x: (
                x[1].pontuacao_total,
                x[1].bilhetes_completos,
                x[1].comprimento_maior_caminho
            ),
            reverse=True
        )
        
        return [jogador_id for jogador_id, _ in jogadores_ordenados]
