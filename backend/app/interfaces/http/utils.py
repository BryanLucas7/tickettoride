from typing import Dict, Optional

from ..models.entities import Jogo

from ..services.game_service import GameService


def processar_fim_acao(game_id: str, game_service: GameService) -> Dict[str, Optional[object]]:
    """
    Extrai a lógica comum de processamento de fim de ação/turno.
    Usado após ações como comprar cartas, conquistar rotas, comprar bilhetes.
    """
    jogo = game_service.get_game(game_id)
    if not jogo:
        return {}

    resultado = {
        "turno_passado": False,
        "jogo_terminou": False,
        "mensagem_fim": None,
        "proximo_jogador": None
    }

    if jogo.estadoCompraCartas.turnoCompleto:
        jogo.estadoCompraCartas.resetar()
        jogo.gerenciadorDeTurnos.nextTurn()

        if jogo.gerenciadorFimDeJogo and jogo.gerenciadorFimDeJogo.ultima_rodada_ativada:
            resultado_fim = jogo.gerenciadorFimDeJogo.processar_turno_jogado()
            if resultado_fim["jogo_terminou"]:
                jogo.encerrar()
                resultado["jogo_terminou"] = True
                resultado["mensagem_fim"] = resultado_fim["mensagem"]

        resultado["turno_passado"] = True
        resultado["proximo_jogador"] = jogo.gerenciadorDeTurnos.jogadorAtual

        game_service.save_game(game_id, jogo)

    return resultado