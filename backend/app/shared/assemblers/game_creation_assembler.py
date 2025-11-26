"""
GameCreationAssembler - Montador de resposta de criação de jogo.

Padrão GRASP: Pure Fabrication
Princípio SRP: Responsável apenas por montar resposta de criação.

Responsabilidades:
- Montar resposta de criação de jogo
- Formatar jogadores iniciais
"""

from typing import Dict, Any, List
from ...core.domain.entities.jogo import Jogo


class GameCreationAssembler:
    """
    Assembler especializado para criação de jogo.
    
    Single Responsibility: Monta apenas resposta de criação
    (informações iniciais do jogo e jogadores).
    """
    
    @staticmethod
    def montar_criacao_jogo(jogo: Jogo, incluir_jogadores_detalhados: bool = True) -> Dict[str, Any]:
        """
        Monta resposta de criação de jogo.
        
        Args:
            jogo: Instância do jogo recém-criado
            incluir_jogadores_detalhados: Se deve incluir detalhes completos
            
        Returns:
            Dict com informações do jogo criado
        """
        jogadores_info = GameCreationAssembler._formatar_jogadores(
            jogo, incluir_jogadores_detalhados
        )
        
        return {
            "game_id": jogo.id,
            "numero_jogadores": len(jogo.gerenciadorDeTurnos.jogadores),
            "iniciado": jogo.estado.iniciado,
            "finalizado": jogo.estado.finalizado,
            "jogadores": jogadores_info
        }
    
    @staticmethod
    def _formatar_jogadores(jogo: Jogo, detalhado: bool) -> List[Dict[str, Any]]:
        """Formata lista de jogadores para resposta de criação."""
        if detalhado:
            return [
                {
                    "id": j.id,
                    "nome": j.nome,
                    "cor": j.cor.value,
                    "trens_disponiveis": len(j.vagoes),
                    "num_cartas": len(j.cartasVagao)
                }
                for j in jogo.gerenciadorDeTurnos.jogadores
            ]
        
        return [
            {
                "id": j.id,
                "nome": j.nome,
                "cor": j.cor.value
            }
            for j in jogo.gerenciadorDeTurnos.jogadores
        ]
