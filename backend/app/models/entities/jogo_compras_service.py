class JogoComprasService:
    """Responsável pelas operações de compra de cartas."""

    def __init__(self, jogo):
        self.jogo = jogo

    def comprarCartaDoBaralhoFechado(self, jogador_id: int) -> dict:
        """Compra uma carta do baralho fechado

        Args:
            jogador_id: ID do jogador que está comprando

        Returns:
            Dict com sucesso, carta comprada e mensagem

        Aplica GRASP Controller: Jogo coordena a ação de compra
        """
        # Verifica se pode comprar do fechado
        if not self.jogo.estadoCompraCartas.podeComprarCartaFechada():
            return {
                "sucesso": False,
                "mensagem": self.jogo.estadoCompraCartas.obterMensagemStatus()
            }

        # Busca jogador
        jogador = next((j for j in self.jogo.gerenciadorDeTurnos.jogadores if j.id == jogador_id), None)
        if not jogador:
            return {"sucesso": False, "mensagem": f"Jogador {jogador_id} não encontrado"}

        # Compra carta do baralho
        carta = self.jogo.gerenciadorDeBaralho.comprarCartaVagaoViewer(visivel=False)

        if not carta:
            return {"sucesso": False, "mensagem": "Baralho vazio"}

        # Adiciona carta ao jogador
        jogador.comprarCartaVagao(carta)

        # Registra compra no estado
        self.jogo.estadoCompraCartas.registrarCompraCartaFechada()

        return {
            "sucesso": True,
            "carta": {"cor": carta.cor.value, "ehLocomotiva": carta.ehLocomotiva},
            "cartasCompradas": self.jogo.estadoCompraCartas.cartasCompradas,
            "turnoCompleto": self.jogo.estadoCompraCartas.turnoCompleto,
            "mensagem": self.jogo.estadoCompraCartas.obterMensagemStatus()
        }

    def comprarCartaAberta(self, jogador_id: int, indice: int) -> dict:
        """Compra uma carta das 5 cartas abertas

        Args:
            jogador_id: ID do jogador que está comprando
            indice: Índice da carta aberta (0-4)

        Returns:
            Dict com sucesso, carta comprada e mensagem

        Aplica GRASP Controller: Jogo coordena a ação de compra
        Aplica GRASP Information Expert: GerenciadorDeBaralho valida e executa compra
        """
        # Busca jogador
        jogador = next((j for j in self.jogo.gerenciadorDeTurnos.jogadores if j.id == jogador_id), None)
        if not jogador:
            return {"sucesso": False, "mensagem": f"Jogador {jogador_id} não encontrado"}

        # Verifica índice válido
        if indice < 0 or indice >= 5:
            return {"sucesso": False, "mensagem": f"Índice inválido: {indice}"}

        # Obtém informação da carta antes de comprar
        cartas_abertas = self.jogo.gerenciadorDeBaralho.obterCartasAbertas()
        if indice >= len(cartas_abertas):
            return {"sucesso": False, "mensagem": "Carta não disponível"}

        carta_desejada = cartas_abertas[indice]

        # Verifica se pode comprar esta carta (regras de locomotiva)
        if not self.jogo.estadoCompraCartas.podeComprarCartaAberta(ehLocomotiva=carta_desejada.ehLocomotiva):
            return {
                "sucesso": False,
                "mensagem": self.jogo.estadoCompraCartas.obterMensagemStatus()
            }

        # Compra carta aberta (repõe automaticamente)
        carta = self.jogo.gerenciadorDeBaralho.comprarCartaVagaoVisivel(indice)

        if not carta:
            return {"sucesso": False, "mensagem": "Erro ao comprar carta"}

        # Adiciona carta ao jogador
        jogador.comprarCartaVagao(carta)

        # Registra compra no estado
        self.jogo.estadoCompraCartas.registrarCompraCartaAberta(ehLocomotiva=carta.ehLocomotiva)

        return {
            "sucesso": True,
            "carta": {"cor": carta.cor.value, "ehLocomotiva": carta.ehLocomotiva},
            "cartasCompradas": self.jogo.estadoCompraCartas.cartasCompradas,
            "turnoCompleto": self.jogo.estadoCompraCartas.turnoCompleto,
            "cartasAbertas": [{"cor": c.cor.value, "ehLocomotiva": c.ehLocomotiva} for c in self.jogo.gerenciadorDeBaralho.obterCartasAbertas()],
            "mensagem": self.jogo.estadoCompraCartas.obterMensagemStatus()
        }

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
            "cartasAbertas": [{"cor": c.cor.value, "ehLocomotiva": c.ehLocomotiva} for c in self.jogo.gerenciadorDeBaralho.obterCartasAbertas()] if self.jogo.gerenciadorDeBaralho else [],
            "mensagem": self.jogo.estadoCompraCartas.obterMensagemStatus()
        }