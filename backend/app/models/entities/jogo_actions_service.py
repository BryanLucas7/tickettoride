class JogoActionsService:
    """Responsável pelas ações gerais do jogo e validações de fim."""

    def __init__(self, jogo):
        self.jogo = jogo

    def jogar(self, acao: str, parametros: dict = None):
        """Executa uma ação de jogo

        Args:
            acao: Tipo de ação (comprar_carta, reivindicar_rota, etc)
            parametros: Parâmetros específicos da ação
        """
        jogador_atual = self.jogo.gerenciadorDeTurnos.getJogadorAtual()

        if acao == "comprar_carta":
            carta = self.jogo.gerenciadorDeBaralho.comprarCartaVagaoViewer()
            if carta:
                jogador_atual.comprarCartaVagao(carta)

        elif acao == "reivindicar_rota":
            if parametros and "rota_id" in parametros:
                rota = self.jogo.tabuleiro.obterRotaPorId(parametros["rota_id"])
                if rota and parametros.get("cartas"):
                    if rota.reivindicarRota(jogador_atual, parametros["cartas"]):
                        jogador_atual.reivindicarRota(rota)
                        # Adiciona pontos baseado no comprimento da rota
                        pontos_rota = {1: 1, 2: 2, 3: 4, 4: 7, 5: 10, 6: 15}
                        jogador_atual.pontuacao += pontos_rota.get(rota.comprimento, 0)

        elif acao == "comprar_bilhetes":
            bilhetes = self.jogo.gerenciadorDeBaralho.comprarBilhetes()
            aceitos = jogador_atual.comprarBilhetesDestino(bilhetes)
            nao_aceitos = [b for b in bilhetes if b not in aceitos]
            self.jogo.gerenciadorDeBaralho.devolverBilhetes(nao_aceitos)

        elif acao == "passar":
            jogador_atual.passarTurno()

    def validarFimDeJogo(self) -> bool:
        """Valida se o jogo chegou ao fim

        Returns:
            True se o jogo deve terminar
        """
        # Fim de jogo quando qualquer jogador tiver 2 ou menos vagões
        for jogador in self.jogo.gerenciadorDeTurnos.jogadores:
            if len(jogador.vagoes) <= 2:
                return True
        return False

    def encerrar(self):
        """Encerra o jogo"""
        self.jogo.finalizado = True
        if self.jogo.placar:
            self.jogo.placar.atualizarPlacar()