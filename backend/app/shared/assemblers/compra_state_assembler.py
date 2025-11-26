"""
Assembler para estado de compra de cartas.

GRASP: Pure Fabrication
- Classe artificial criada para responsabilidade de formatação

Refatoração SRP: Extraído de JogoComprasService.obterEstadoCompra()
para separar responsabilidade de formatação da lógica de compra.

Responsabilidades:
- Formatar estado de compra para resposta da API
- Centralizar estrutura de dados de estado de compra
"""

from typing import Dict, Any, List, TYPE_CHECKING

if TYPE_CHECKING:
    from ...core.domain.entities.jogo import Jogo
    from ...core.domain.managers.estado_compra_cartas import EstadoCompraCartas


class CompraStateAssembler:
    """
    Assembler para formatação de estado de compra.
    
    Pure Fabrication (GRASP): Classe artificial para centralizar formatação.
    
    Responsabilidade única (SRP): Apenas formata estado de compra.
    
    Exemplo:
        >>> estado = CompraStateAssembler.montar(jogo)
        >>> # {"cartasCompradas": 1, "turnoCompleto": False, ...}
    """
    
    @staticmethod
    def montar(jogo: 'Jogo') -> Dict[str, Any]:
        """
        Monta resposta formatada do estado de compra.
        
        Args:
            jogo: Instância do jogo
            
        Returns:
            Dict com estado de compra formatado:
            - cartasCompradas: int - Número de cartas compradas no turno
            - comprouLocomotivaDasAbertas: bool - Se comprou locomotiva das abertas
            - turnoCompleto: bool - Se o turno de compra está completo
            - podeComprarFechada: bool - Se pode comprar do baralho
            - cartasAbertas: List - Cartas abertas formatadas
            - mensagem: str - Mensagem de status atual
        """
        from ..formatters import EntityFormatters
        
        estado_compra = jogo.estado.estado_compra
        gerenciador = jogo.gerenciadorDeBaralhoVagoes
        
        return {
            "cartasCompradas": estado_compra.cartasCompradas,
            "comprouLocomotivaDasAbertas": estado_compra.comprouLocomotivaDasAbertas,
            "turnoCompleto": estado_compra.turnoCompleto,
            "podeComprarFechada": estado_compra.podeComprarCartaFechada(),
            "cartasAbertas": CompraStateAssembler._formatar_cartas_abertas(gerenciador),
            "mensagem": estado_compra.obterMensagemStatus()
        }
    
    @staticmethod
    def _formatar_cartas_abertas(gerenciador) -> List[Dict[str, Any]]:
        """
        Formata cartas abertas para resposta.
        
        Args:
            gerenciador: Gerenciador de baralho de vagões
            
        Returns:
            Lista de cartas formatadas
        """
        from ..formatters import EntityFormatters
        
        if not gerenciador:
            return []
        
        cartas = gerenciador.obterCartasAbertas()
        return [EntityFormatters.formatar_carta_vagao(c) for c in cartas]
    
    @staticmethod
    def montar_resumo(jogo: 'Jogo') -> Dict[str, Any]:
        """
        Monta resumo simplificado do estado de compra.
        
        Útil para respostas que não precisam de todos os detalhes.
        
        Args:
            jogo: Instância do jogo
            
        Returns:
            Dict com resumo do estado
        """
        estado_compra = jogo.estado.estado_compra
        
        return {
            "cartasCompradas": estado_compra.cartasCompradas,
            "turnoCompleto": estado_compra.turnoCompleto,
            "mensagem": estado_compra.obterMensagemStatus()
        }
