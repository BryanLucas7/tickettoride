from fastapi import HTTPException

from ..support.responses import success_response, error_response
from ..support.formatters import format_card, format_cards
from ....shared.validators import GameValidators


class JogoComprasService:
    """Responsável pelas operações de compra de cartas."""

    def __init__(self, jogo):
        self.jogo = jogo

    def comprarCartaDoBaralhoFechado(self, jogador_id: str) -> dict:
        """Compra uma carta do baralho fechado

        Args:
            jogador_id: ID do jogador que está comprando

        Returns:
            Dict com sucesso, carta comprada e mensagem

        Aplica GRASP Controller: Jogo coordena a ação de compra
        """
        # Verifica se pode comprar do fechado
        if not self.jogo.estadoCompraCartas.podeComprarCartaFechada():
            return error_response(self.jogo.estadoCompraCartas.obterMensagemStatus())

        # Busca jogador e valida existência
        jogador = self.jogo.gerenciadorDeTurnos.obter_jogador_por_id(jogador_id)
        if not jogador:
            return error_response(f"Jogador {jogador_id} não encontrado")

        # Compra carta do baralho
        carta = self.jogo.gerenciadorDeBaralho.comprarCartaVagaoViewer(visivel=False)

        if not carta:
            return error_response("Baralho vazio")

        # Adiciona carta ao jogador
        jogador.comprarCartaVagao(carta)

        # Registra compra no estado
        self.jogo.estadoCompraCartas.registrarCompraCartaFechada()

        # Edge case: se não há mais cartas possíveis para compra, encerra turno automaticamente
        if not self.jogo.estadoCompraCartas.turnoCompleto and not self._ha_opcao_de_compra():
            self.jogo.estadoCompraCartas.turnoCompleto = True

        return success_response(
            self.jogo.estadoCompraCartas.obterMensagemStatus(),
            carta=format_card(carta),
            cartasCompradas=self.jogo.estadoCompraCartas.cartasCompradas,
            turnoCompleto=self.jogo.estadoCompraCartas.turnoCompleto
        )

    def comprarCartaAberta(self, jogador_id: str, indice: int) -> dict:
        """Compra uma carta das 5 cartas abertas

        Args:
            jogador_id: ID do jogador que está comprando
            indice: Índice da carta aberta (0-4)

        Returns:
            Dict com sucesso, carta comprada e mensagem

        Aplica GRASP Controller: Jogo coordena a ação de compra
        Aplica GRASP Information Expert: GerenciadorDeBaralho valida e executa compra
        """
        # Busca jogador e valida existência
        jogador = self.jogo.gerenciadorDeTurnos.obter_jogador_por_id(jogador_id)
        if not jogador:
            return error_response(f"Jogador {jogador_id} não encontrado")

        # Valida índice usando validador centralizado
        cartas_abertas = self.jogo.gerenciadorDeBaralho.obterCartasAbertas()
        try:
            GameValidators.validar_indice(indice, len(cartas_abertas), "carta aberta")
        except HTTPException as e:
            return error_response(e.detail)

        carta_desejada = cartas_abertas[indice]

        # Verifica se pode comprar esta carta (regras de locomotiva)
        if not self.jogo.estadoCompraCartas.podeComprarCartaAberta(ehLocomotiva=carta_desejada.ehLocomotiva):
            return error_response(self.jogo.estadoCompraCartas.obterMensagemStatus())

        # Compra carta aberta (repõe automaticamente)
        carta = self.jogo.gerenciadorDeBaralho.comprarCartaVagaoVisivel(indice)

        if not carta:
            return error_response("Erro ao comprar carta")

        # Adiciona carta ao jogador
        jogador.comprarCartaVagao(carta)

        # Registra compra no estado
        self.jogo.estadoCompraCartas.registrarCompraCartaAberta(ehLocomotiva=carta.ehLocomotiva)

        # Edge case: se não há mais cartas possíveis para compra, encerra turno automaticamente
        if not self.jogo.estadoCompraCartas.turnoCompleto and not self._ha_opcao_de_compra():
            self.jogo.estadoCompraCartas.turnoCompleto = True

        return success_response(
            self.jogo.estadoCompraCartas.obterMensagemStatus(),
            carta=format_card(carta),
            cartasCompradas=self.jogo.estadoCompraCartas.cartasCompradas,
            turnoCompleto=self.jogo.estadoCompraCartas.turnoCompleto,
            cartasAbertas=format_cards(self.jogo.gerenciadorDeBaralho.obterCartasAbertas())
        )

    def obterEstadoCompra(self) -> dict:
        """Retorna o estado atual de compra de cartas

        Returns:
            Dict com informações do estado de compra
        """
        return {
            "cartasCompradas": self.jogo.estadoCompraCartas.cartasCompradas,
            "comprouLocomotivaDasAbertas": self.jogo.estadoCompraCartas.comprouLocomotivaDasAbertas,
            "turnoCompleto": self.jogo.estadoCompraCartas.turnoCompleto,
            "podeComprarFechada": self.jogo.estadoCompraCartas.podeComprarCartaFechada(),
            "cartasAbertas": format_cards(self.jogo.gerenciadorDeBaralho.obterCartasAbertas()) if self.jogo.gerenciadorDeBaralho else [],
            "mensagem": self.jogo.estadoCompraCartas.obterMensagemStatus()
        }

    def _ha_opcao_de_compra(self) -> bool:
        """
        Verifica se ainda existe alguma carta que possa ser comprada neste turno.
        Considera regras do estado (locomotiva, limite 2 cartas) e disponibilidade.
        """
        estado = self.jogo.estadoCompraCartas

        if estado.turnoCompleto:
            return False

        baralho = self.jogo.gerenciadorDeBaralho

        # Há carta fechada disponível no baralho/descarte e regra permite?
        if estado.podeComprarCartaFechada():
            if (baralho.baralhoVagoes and len(baralho.baralhoVagoes.cartas) > 0) or baralho.descarteVagoes:
                return True

        # Há alguma carta aberta permitida pelo estado?
        for carta in baralho.obterCartasAbertas():
            if estado.podeComprarCartaAberta(ehLocomotiva=carta.ehLocomotiva):
                return True

        return False
