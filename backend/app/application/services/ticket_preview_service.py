"""
Service para pré-visualização de bilhetes.

Extrai lógica do endpoint preview_tickets em player_routes.py.

Responsabilidades:
- Validar quantidade de bilhetes (1-3)
- Verificar disponibilidade no baralho
- Gerenciar bilhetes reservados (retornar existentes ou criar novos)
- Sortear bilhetes do baralho
- Reservar bilhetes para confirmação posterior

GRASP:
- Single Responsibility: Apenas pré-visualização de bilhetes
- Controller: Orquestra validação, sorteio e reserva
- Information Expert: Conhece regras de preview
- DRY: Centraliza lógica que estava no endpoint

Refatoração DRY:
- Move lógica de preview_tickets do endpoint para serviço reutilizável
- Usa BilheteHelpers para validações
- Usa EntityFormatters para formatação consistente
"""

from typing import Dict, Any, List
from ...core.domain.entities.jogo import Jogo
from ...core.domain.entities.bilhete_destino import BilheteDestino
from ...shared.bilhete_helpers import BilheteHelpers
from ...shared.formatters import EntityFormatters


class TicketPreviewService:
    """
    Serviço para pré-visualização de bilhetes antes da compra.
    
    Gerencia o fluxo de sorteio e reserva de bilhetes, mantendo-os
    separados até a confirmação da compra pelo jogador.
    """
    
    QUANTIDADE_MINIMA = 1
    QUANTIDADE_MAXIMA = 3
    
    @staticmethod
    def preview_bilhetes(
        jogo: Jogo,
        player_id: str,
        quantidade: int = 3
    ) -> Dict[str, Any]:
        """
        Sorteia bilhetes para preview ou retorna bilhetes já reservados.
        
        Args:
            jogo: Instância do jogo
            player_id: ID do jogador
            quantidade: Quantidade de bilhetes desejada (1-3)
            
        Returns:
            Dict com:
                - success: bool
                - tickets: Lista de bilhetes com índice
                - quantidade: Número de bilhetes retornados
                - message: Mensagem de erro (se houver)
                
        Raises:
            ValueError: Se validação falhar
        """
        # Validar quantidade
        TicketPreviewService._validar_quantidade(quantidade)
        
        # Validar baralho inicializado
        if not jogo.gerenciadorDeBaralho:
            raise ValueError("Deck not initialized")
        
        # Verificar se já existem bilhetes reservados
        bilhetes_reservados = jogo.obter_bilhetes_reservados(player_id)
        
        if bilhetes_reservados:
            # Retornar bilhetes já reservados
            return TicketPreviewService._formatar_resposta(bilhetes_reservados)
        
        # Sortear novos bilhetes
        bilhetes_reservados = TicketPreviewService._sortear_bilhetes(
            jogo, 
            quantidade
        )
        
        # Reservar bilhetes para o jogador
        jogo.reservar_bilhetes(player_id, bilhetes_reservados)
        
        return TicketPreviewService._formatar_resposta(bilhetes_reservados)
    
    @staticmethod
    def _validar_quantidade(quantidade: int) -> None:
        """
        Valida quantidade de bilhetes solicitada.
        
        Args:
            quantidade: Número de bilhetes
            
        Raises:
            ValueError: Se quantidade for inválida
        """
        BilheteHelpers.validar_quantidade_minima(
            quantidade,
            TicketPreviewService.QUANTIDADE_MINIMA,
            "tickets"
        )
        BilheteHelpers.validar_quantidade_maxima(
            quantidade,
            TicketPreviewService.QUANTIDADE_MAXIMA,
            "tickets"
        )
    
    @staticmethod
    def _sortear_bilhetes(
        jogo: Jogo,
        quantidade: int
    ) -> List[BilheteDestino]:
        """
        Sorteia bilhetes do baralho.
        
        Args:
            jogo: Instância do jogo
            quantidade: Quantidade desejada de bilhetes
            
        Returns:
            Lista de bilhetes sorteados
            
        Raises:
            ValueError: Se não houver bilhetes disponíveis
        """
        cartas_disponiveis = jogo.gerenciadorDeBaralho.baralhoBilhetes.cartas
        
        if not cartas_disponiveis:
            raise ValueError("No tickets available")
        
        # Ajustar quantidade ao disponível
        quantidade_real = min(quantidade, len(cartas_disponiveis))
        bilhetes_sorteados = []
        
        for _ in range(quantidade_real):
            bilhete = jogo.gerenciadorDeBaralho.baralhoBilhetes.comprar()
            if bilhete:
                bilhetes_sorteados.append(bilhete)
        
        if not bilhetes_sorteados:
            raise ValueError("No tickets available")
        
        return bilhetes_sorteados
    
    @staticmethod
    def _formatar_resposta(
        bilhetes: List[BilheteDestino]
    ) -> Dict[str, Any]:
        """
        Formata resposta com bilhetes para preview.
        
        Args:
            bilhetes: Lista de bilhetes
            
        Returns:
            Dict formatado para resposta da API
        """
        return {
            "success": True,
            "tickets": [
                {
                    "index": indice,
                    **EntityFormatters.formatar_bilhete(bilhete, formato="compacto")
                }
                for indice, bilhete in enumerate(bilhetes)
            ],
            "quantidade": len(bilhetes)
        }
