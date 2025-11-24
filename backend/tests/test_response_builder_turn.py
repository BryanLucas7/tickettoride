"""Testes para helpers de turno do ResponseBuilder."""

from backend.app.shared.response_builder import ResponseBuilder


class TestResponseBuilderSuccessWithTurn:
    """Testes para ResponseBuilder.success_with_turn()."""
    
    def test_success_with_turn_cria_resposta_completa(self):
        """Deve criar resposta completa com turno em uma chamada."""
        resultado_turno = {
            "proximo_jogador": "2",
            "jogo_terminou": False,
            "mensagem_fim": None
        }
        
        resultado = ResponseBuilder.success_with_turn(
            "Rota conquistada",
            resultado_turno,
            points=10,
            trains_remaining=27
        )
        
        # Campos base
        assert resultado["success"] is True
        assert resultado["message"] == "Rota conquistada"
        
        # Campos de turno
        assert resultado["turn_completed"] is True
        assert resultado["turno_passado"] is True
        assert resultado["next_player"] == "2"
        assert resultado["jogo_terminou"] is False
        assert resultado["mensagem_fim"] is None
        
        # Campos extras
        assert resultado["points"] == 10
        assert resultado["trains_remaining"] == 27
    
    def test_success_with_turn_jogo_terminado(self):
        """Deve incluir mensagem de fim quando jogo termina."""
        resultado_turno = {
            "proximo_jogador": "1",
            "jogo_terminou": True,
            "mensagem_fim": "Última rodada concluída!"
        }
        
        resultado = ResponseBuilder.success_with_turn(
            "Bilhetes comprados",
            resultado_turno,
            tickets_kept=2
        )
        
        assert resultado["jogo_terminou"] is True
        assert resultado["mensagem_fim"] == "Última rodada concluída!"
        assert resultado["tickets_kept"] == 2
