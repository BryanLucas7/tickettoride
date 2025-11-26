"""
JogoComprasService - Serviço interno para operações de compra de cartas.

NOTA ARQUITETURAL:
Este é um "inner service" da entidade Jogo, não um serviço de aplicação.
Está em entities/ porque:
1. É parte intrínseca da entidade Jogo (delegação interna)
2. Tem dependência bidirecional com Jogo (recebe self.jogo)
3. Não orquestra múltiplas entidades externas

Para compra de bilhetes (serviço de aplicação), use:
- application/services/ticket_purchase_service.py

Padrão GRASP: Controller (Jogo delega controle de compras)
Princípio SRP: 
- JogoComprasService: execução de compras
- CompraValidator: validação de regras (refatorado para Composite Pattern)
"""

from ..support.responses import success_response, error_response
from ..support.formatters import format_card, format_cards
from ..validators import CompraValidator  # Refatorado: agora usa Composite


class JogoComprasService:
    """Responsável pela execução de operações de compra de cartas.
    
    Validações são delegadas para CompraValidator (SRP).
    """

    def __init__(self, jogo):
        self.jogo = jogo
        self.validator = CompraValidator(jogo)

    def _finalizar_compra(self, jogador, carta, **extras) -> dict:
        """Método auxiliar para finalizar uma compra de carta.
        
        Centraliza a lógica comum entre compra de carta fechada e aberta:
        - Adiciona carta ao jogador
        - Verifica encerramento automático de turno
        - Formata resposta de sucesso
        
        Args:
            jogador: Jogador que está comprando
            carta: Carta comprada
            **extras: Campos adicionais para a resposta (ex: cartasAbertas)
            
        Returns:
            Dict com sucesso, carta e informações de turno
        """
        jogador.comprarCartaVagao(carta)
        
        # Edge case: se não há mais cartas possíveis para compra, encerra turno automaticamente
        # Usa validator.ha_opcao_de_compra() (SRP - validação no validator)
        if not self.jogo.estado.estado_compra.turnoCompleto and not self.validator.ha_opcao_de_compra():
            self.jogo.estado.estado_compra.turnoCompleto = True
        
        return success_response(
            self.jogo.estado.estado_compra.obterMensagemStatus(),
            carta=format_card(carta),
            cartasCompradas=self.jogo.estado.estado_compra.cartasCompradas,
            turnoCompleto=self.jogo.estado.estado_compra.turnoCompleto,
            **extras
        )

    def comprarCartaDoBaralhoFechado(self, jogador_id: str) -> dict:
        """Compra uma carta do baralho fechado

        Args:
            jogador_id: ID do jogador que está comprando

        Returns:
            Dict com sucesso, carta comprada e mensagem

        Aplica GRASP Controller: Jogo coordena a ação de compra
        SRP: Validações delegadas para CompraValidator
        """
        # Validação completa usando CompraValidator (SRP)
        resultado = self.validator.validar_compra_carta_fechada_completa(jogador_id)
        if resultado.invalido:
            return error_response(resultado.erro)
        
        jogador = resultado.jogador

        # Compra carta do baralho
        carta = self.jogo.gerenciadorDeBaralhoVagoes.comprarCartaVagaoViewer(visivel=False)

        if not carta:
            return error_response("Baralho vazio")

        # Registra compra no estado
        self.jogo.estado.estado_compra.registrarCompraCartaFechada()

        # Finaliza compra usando método auxiliar
        return self._finalizar_compra(jogador, carta)

    def comprarCartaAberta(self, jogador_id: str, indice: int) -> dict:
        """Compra uma carta das 5 cartas abertas

        Args:
            jogador_id: ID do jogador que está comprando
            indice: Índice da carta aberta (0-4)

        Returns:
            Dict com sucesso, carta comprada e mensagem

        Aplica GRASP Controller: Jogo coordena a ação de compra
        Aplica GRASP Information Expert: GerenciadorDeBaralho valida e executa compra
        SRP: Validações delegadas para CompraValidator
        """
        # Validação completa usando CompraValidator (SRP)
        resultado, carta_desejada = self.validator.validar_compra_carta_aberta_completa(
            jogador_id, indice
        )
        if resultado.invalido:
            return error_response(resultado.erro)
        
        jogador = resultado.jogador

        # Compra carta aberta (repõe automaticamente)
        carta = self.jogo.gerenciadorDeBaralhoVagoes.comprarCartaVagaoVisivel(indice)

        if not carta:
            return error_response("Erro ao comprar carta")

        # Registra compra no estado
        self.jogo.estado.estado_compra.registrarCompraCartaAberta(ehLocomotiva=carta.ehLocomotiva)

        # Finaliza compra usando método auxiliar (inclui cartas abertas atualizadas)
        return self._finalizar_compra(
            jogador, 
            carta,
            cartasAbertas=format_cards(self.jogo.gerenciadorDeBaralhoVagoes.obterCartasAbertas())
        )

    def obterEstadoCompra(self) -> dict:
        """Retorna o estado atual de compra de cartas.

        Refatoração SRP: Formatação delegada para CompraStateAssembler.

        Returns:
            Dict com informações do estado de compra
        """
        from app.shared.assemblers import CompraStateAssembler
        return CompraStateAssembler.montar(self.jogo)
