"""
RouteAssembler - Montador de painel de rotas.

Padrão GRASP: Pure Fabrication
Princípio SRP: Responsável apenas por montar informações de rotas.

Responsabilidades:
- Montar painel de rotas do tabuleiro
- Formatar rotas com proprietário
- Contabilizar rotas livres/conquistadas
"""

from typing import Dict, Any
from ...core.domain.entities.jogo import Jogo
from ..formatters import EntityFormatters


class RouteAssembler:
    """
    Assembler especializado para rotas do tabuleiro.
    
    Single Responsibility: Monta apenas informações de rotas
    (lista de rotas, estatísticas, proprietários).
    """
    
    @staticmethod
    def montar_painel_rotas(jogo: Jogo, incluir_proprietario_detalhes: bool = True) -> Dict[str, Any]:
        """
        Monta painel de rotas do tabuleiro.
        
        Args:
            jogo: Instância do jogo
            incluir_proprietario_detalhes: Se deve incluir nome e cor do proprietário
            
        Returns:
            Dict com lista de rotas formatadas
        """
        rotas_formatadas = []
        rotas_livres = 0
        rotas_conquistadas = 0
        
        for rota in jogo.tabuleiro.rotas:
            rota_info = RouteAssembler._formatar_rota_com_proprietario(
                rota, incluir_proprietario_detalhes
            )
            rotas_formatadas.append(rota_info)
            
            if rota.proprietario:
                rotas_conquistadas += 1
            else:
                rotas_livres += 1
        
        return {
            "game_id": jogo.id,
            "total_rotas": len(jogo.tabuleiro.rotas),
            "rotas_livres": rotas_livres,
            "rotas_conquistadas": rotas_conquistadas,
            "rotas": rotas_formatadas
        }
    
    @staticmethod
    def _formatar_rota_com_proprietario(rota, incluir_detalhes: bool) -> Dict[str, Any]:
        """Formata uma rota incluindo detalhes do proprietário se solicitado."""
        rota_info = EntityFormatters.formatar_rota(rota)
        
        if incluir_detalhes and rota.proprietario:
            rota_info["proprietario_nome"] = rota.proprietario.nome
            rota_info["proprietario_cor"] = rota.proprietario.cor.value
        
        return rota_info
