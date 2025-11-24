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
        caminho_cidades: Optional[List[str]] = None
        
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
                # Captura caminho detalhado do primeiro líder (suficiente para exibir)
                if caminho_cidades is None:
                    _, rotas_caminho = self.calculator.encontrar_maior_caminho(
                        jogo.rotas_do_jogador(jogador)
                    )
                    caminho_cidades = self._rotas_para_caminho_cidades(rotas_caminho)
        
        return MaiorCaminhoStatusResponse(
            comprimento=int(maior_comprimento),
            lideres=lideres_response,
            caminho=caminho_cidades
        )

    def _rotas_para_caminho_cidades(self, rotas_caminho):
        """Converte sequência de rotas em lista de nomes de cidades na ordem."""
        if not rotas_caminho:
            return []

        caminho_cidades = []
        # inicia com a primeira rota
        primeira = rotas_caminho[0]
        caminho_cidades.append(primeira.cidadeA.nome)
        caminho_cidades.append(primeira.cidadeB.nome)

        for rota in rotas_caminho[1:]:
            if rota.cidadeA.nome == caminho_cidades[-1]:
                caminho_cidades.append(rota.cidadeB.nome)
            elif rota.cidadeB.nome == caminho_cidades[-1]:
                caminho_cidades.append(rota.cidadeA.nome)
            else:
                # se não encaixar, apenas adiciona extremidades (fallback)
                caminho_cidades.append(rota.cidadeA.nome)
                caminho_cidades.append(rota.cidadeB.nome)

        return caminho_cidades
