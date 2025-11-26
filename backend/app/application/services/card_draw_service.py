"""
Service para compra de cartas fechadas e abertas.

Extrai lógica dos endpoints draw_closed_card e draw_open_card em player_routes.py.

Responsabilidades:
- Executar compra de carta (fechada/aberta)
- Formatar response para API (success, card, etc.)
- Verificar e auto-passar turno se necessário via GameActionService
- Manter SRP: apenas lógica de draw de cartas

GRASP:
- Information Expert: conhece regras de compra de cartas
- Pure Fabrication: service dedicado para evitar duplicação
"""
from typing import Dict, Any
from ...core.domain.entities.jogo import Jogo
from .game_action_service import GameActionService
from ...shared.response_builder import ResponseBuilder


class CardDrawService:
    @staticmethod
    def _processar_resultado_compra(
        jogo: Jogo,
        resultado_compra: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Processa resultado de compra de carta (fechada ou aberta).
        
        Centraliza lógica comum de normalização, formatação e turno.
        Elimina ~30 linhas de código duplicado entre comprar_carta_fechada 
        e comprar_carta_aberta.
        
        Args:
            jogo: Instância do jogo
            resultado_compra: Resultado bruto da compra
            
        Returns:
            Response formatado com informações de turno
            
        Example:
            >>> resultado = jogo.compras.comprarCartaDoBaralhoFechado(player_id)
            >>> return CardDrawService._processar_resultado_compra(jogo, resultado)
        """
        # Resultado já vem no formato correto (success/message) do domínio
        resultado_normalizado = resultado_compra
        
        if not resultado_normalizado["success"]:
            return ResponseBuilder.error(resultado_normalizado["message"])
        
        # Carta já vem formatada do domínio (via format_card)
        carta_formatted = resultado_compra.get("carta", {})
        
        # Monta response base
        response: Dict[str, Any] = {
            "success": True,
            "message": resultado_normalizado["message"],
            "card": carta_formatted,
        }
        
        # Usa método centralizado para adicionar informações de turno
        action_service = GameActionService()
        return action_service.formatar_resposta_com_fim_turno(jogo, response)
    
    @staticmethod
    def comprar_carta_fechada(jogo: Jogo, player_id: str) -> Dict[str, Any]:
        """
        Compra carta fechada do baralho e processa turno completo se necessário.
        
        Retorna formato pronto para API response.
        """
        resultado_compra = jogo.compras.comprarCartaDoBaralhoFechado(player_id)
        return CardDrawService._processar_resultado_compra(jogo, resultado_compra)

    @staticmethod
    def comprar_carta_aberta(jogo: Jogo, player_id: str, card_index: int) -> Dict[str, Any]:
        """
        Compra carta aberta pelo índice e processa turno completo se necessário.
        
        Retorna formato pronto para API response.
        """
        resultado_compra = jogo.compras.comprarCartaAberta(player_id, card_index)
        return CardDrawService._processar_resultado_compra(jogo, resultado_compra)