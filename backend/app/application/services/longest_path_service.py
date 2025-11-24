"""
Service para centralizar cálculos de maior caminho contínuo.

PADRÃO GRASP: Pure Fabrication
- LongestPathService encapsula lógica de cálculo de maior caminho
- Evita duplicação entre game_routes.py e pontuacao_final_calculator.py

PADRÃO GRASP: Information Expert
- Service conhece como calcular maior caminho para todos jogadores
- Service determina líderes baseado nos comprimentos calculados
"""

from dataclasses import dataclass, field
from typing import Dict, Optional
from ...core.domain.calculators.longest_path import LongestPathCalculator
from ...core.domain.entities import Jogo
from ...adapters.inbound.http.schemas import (
    MaiorCaminhoLeaderResponse,
    MaiorCaminhoStatusResponse,
)


@dataclass
class LongestPathService:
    """
    Service para cálculo centralizado de maior caminho.
    
    Responsabilidades:
    - Calcular maior caminho para todos os jogadores
    - Gerar status completo do maior caminho
    
    GRASP Principles:
    - Pure Fabrication: Serviço de infraestrutura
    - Low Coupling: Depende apenas de LongestPathCalculator
    - High Cohesion: Focado apenas em maior caminho
    """
    
    calculator: LongestPathCalculator = field(default_factory=LongestPathCalculator)
    
    def calcular_para_todos_jogadores(self, jogo: Jogo) -> Dict[str, int]:
        """
        Calcula o maior caminho para todos os jogadores.
        
        Args:
            jogo: Instância do jogo
            
        Returns:
            Dicionário {jogador_id: comprimento_maior_caminho}
        """
        resultados = {}
        
        for jogador in jogo.gerenciadorDeTurnos.jogadores:
            rotas_jogador = jogo.rotas_do_jogador(jogador)
            
            comprimento = 0
            if rotas_jogador:
                comprimento = self.calculator.calcular_maior_caminho(rotas_jogador)
            
            resultados[jogador.id] = comprimento
        
        return resultados
    
    def calcular_status(self, jogo: Jogo) -> Optional[MaiorCaminhoStatusResponse]:
        """
        Calcula o status completo do maior caminho para exibição.
        
        Args:
            jogo: Instância do jogo
            
        Returns:
            MaiorCaminhoStatusResponse com líderes e comprimento, ou None se inválido
        """
        if not jogo or not jogo.tabuleiro:
            return None
        
        comprimentos = self.calcular_para_todos_jogadores(jogo)
        
        if not comprimentos:
            return None
        
        maior_comprimento = max(comprimentos.values())
        
        lideres_response = []
        for jogador in jogo.gerenciadorDeTurnos.jogadores:
            if comprimentos[jogador.id] == maior_comprimento:
                lideres_response.append(
                    MaiorCaminhoLeaderResponse(
                        jogador_id=jogador.id,
                        jogador_nome=jogador.nome,
                        jogador_cor=jogador.cor.value if hasattr(jogador.cor, "value") else jogador.cor
                    )
                )
        
        return MaiorCaminhoStatusResponse(
            comprimento=int(maior_comprimento),
            lideres=lideres_response
        )
