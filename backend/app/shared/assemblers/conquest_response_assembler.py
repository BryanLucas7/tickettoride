"""
Assembler para respostas de conquista de rota.

GRASP: Pure Fabrication
SRP: Única responsabilidade - montar estrutura de resposta para conquista.

Extraído de RouteConquestService para separar:
- Lógica de negócio (service)
- Formatação de resposta (assembler)
"""

from typing import Dict, Any, Optional

from ..response_builder import ResponseBuilder
from ...core.domain.support.types import ResultadoTurno


class ConquestResponseAssembler:
    """
    Monta resposta padronizada para conquista de rotas.
    
    Separa formatação de resposta da lógica de negócio,
    permitindo que o service foque apenas em orquestração.
    
    Uso típico:
        return ConquestResponseAssembler.montar_sucesso(
            mensagem="Rota conquistada!",
            resultado_turno=resultado_turno,
            pontos_ganhos=10,
            trens_restantes=35
        )
    """
    
    @staticmethod
    def montar_sucesso(
        mensagem: str,
        resultado_turno: ResultadoTurno,
        pontos_ganhos: int,
        trens_restantes: int,
        fim_de_jogo_ativado: bool = False,
        alerta_fim_jogo: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Monta resposta de sucesso para conquista.
        
        Args:
            mensagem: Mensagem descritiva da conquista
            resultado_turno: Dados do turno passado (próximo jogador, etc)
            pontos_ganhos: Pontos obtidos na conquista
            trens_restantes: Trens restantes do jogador
            fim_de_jogo_ativado: Se fim de jogo foi ativado
            alerta_fim_jogo: Mensagem de alerta de fim (opcional)
            
        Returns:
            Dict formatado para resposta HTTP com estrutura:
            {
                "success": True,
                "message": str,
                "turn_completed": True,
                "next_player": str,
                "points": int,
                "trains_remaining": int,
                "game_ending": bool,
                "alerta_fim_jogo": str | None,
                ...
            }
        """
        response = ResponseBuilder.success_with_turn(
            message=mensagem,
            resultado_turno=resultado_turno,
            points=pontos_ganhos,
            trains_remaining=trens_restantes,
            game_ending=fim_de_jogo_ativado
        )
        
        if alerta_fim_jogo:
            response["alerta_fim_jogo"] = alerta_fim_jogo
        
        return response
    
    @staticmethod
    def montar_erro(
        mensagem: str, 
        codigo: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Monta resposta de erro para conquista.
        
        Args:
            mensagem: Mensagem de erro
            codigo: Código identificador do erro (opcional)
            
        Returns:
            Dict formatado para resposta de erro
        """
        return ResponseBuilder.error(mensagem, code=codigo)
