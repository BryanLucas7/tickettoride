"""
Testes para padronização de respostas de turno via ResponseBuilder.
"""

from app.shared.response_builder import ResponseBuilder


class TestSuccessWithTurn:
    """Testes para ResponseBuilder.success_with_turn()"""
    
    def test_success_with_turn_turno_normal(self):
        """Testa resposta com turno normal (jogo continua)."""
        resultado_turno = {
            "proximo_jogador": "player-2",
            "jogo_terminou": False,
            "mensagem_fim": None
        }
        
        response = ResponseBuilder.success_with_turn(
            message="Rota conquistada",
            resultado_turno=resultado_turno,
            points=4,
            trains_remaining=10
        )
        
        # Campos básicos
        assert response["success"] is True
        assert response["message"] == "Rota conquistada"
        
        # Campos de turno
        assert response["turn_completed"] is True
        assert response["turno_passado"] is True
        assert response["next_player"] == "player-2"
        assert response["jogo_terminou"] is False
        assert response["mensagem_fim"] is None
        
        # Campos específicos da ação
        assert response["points"] == 4
        assert response["trains_remaining"] == 10
    
    def test_success_with_turn_ultima_rodada(self):
        """Testa resposta quando última rodada é ativada."""
        resultado_turno = {
            "proximo_jogador": "player-3",
            "jogo_terminou": True,
            "mensagem_fim": "Última rodada! Um jogador tem 2 ou menos trens."
        }
        
        response = ResponseBuilder.success_with_turn(
            message="Bilhetes comprados",
            resultado_turno=resultado_turno,
            tickets_kept=2,
            tickets_returned=1
        )
        
        assert response["success"] is True
        assert response["message"] == "Bilhetes comprados"
        assert response["turno_passado"] is True
        assert response["next_player"] == "player-3"
        assert response["jogo_terminou"] is True
        assert response["mensagem_fim"] == "Última rodada! Um jogador tem 2 ou menos trens."
        assert response["tickets_kept"] == 2
        assert response["tickets_returned"] == 1
    
    def test_success_with_turn_fim_de_jogo(self):
        """Testa resposta quando jogo termina."""
        resultado_turno = {
            "proximo_jogador": "player-1",
            "jogo_terminou": True,
            "mensagem_fim": "Jogo finalizado!"
        }
        
        response = ResponseBuilder.success_with_turn(
            message="Turno passado",
            resultado_turno=resultado_turno
        )
        
        assert response["jogo_terminou"] is True
        assert response["mensagem_fim"] == "Jogo finalizado!"
    
    def test_success_with_turn_sem_campos_extras(self):
        """Testa que funciona sem campos específicos da ação."""
        resultado_turno = {
            "proximo_jogador": "player-1",
            "jogo_terminou": False,
            "mensagem_fim": None
        }
        
        response = ResponseBuilder.success_with_turn(
            message="Ação realizada",
            resultado_turno=resultado_turno
        )
        
        # Deve ter apenas campos básicos + turno
        assert "success" in response
        assert "message" in response
        assert "turn_completed" in response
        assert "turno_passado" in response
        assert "next_player" in response
        assert "jogo_terminou" in response
        assert "mensagem_fim" in response
        assert len(response) == 7
    
    def test_success_with_turn_multiplos_campos_extras(self):
        """Testa que aceita múltiplos campos extras."""
        resultado_turno = {
            "proximo_jogador": "player-4",
            "jogo_terminou": False,
            "mensagem_fim": None
        }
        
        response = ResponseBuilder.success_with_turn(
            message="Ação complexa",
            resultado_turno=resultado_turno,
            campo1="valor1",
            campo2=123,
            campo3=True,
            campo4=["lista", "de", "valores"]
        )
        
        assert response["campo1"] == "valor1"
        assert response["campo2"] == 123
        assert response["campo3"] is True
        assert response["campo4"] == ["lista", "de", "valores"]


class TestCenariosReais:
    """Testes baseados em cenários reais de uso"""
    
    def test_cenario_conquista_rota(self):
        """Simula resposta de conquista de rota."""
        resultado_turno = {
            "proximo_jogador": "player-2",
            "jogo_terminou": False,
            "mensagem_fim": None
        }
        
        response = ResponseBuilder.success_with_turn(
            message="Rota São Paulo - Rio de Janeiro conquistada",
            resultado_turno=resultado_turno,
            points=4,
            trains_remaining=35,
            game_ending=False
        )
        
        assert response["success"] is True
        assert response["points"] == 4
        assert response["trains_remaining"] == 35
        assert response["game_ending"] is False
        assert response["next_player"] == "player-2"
    
    def test_cenario_compra_bilhetes(self):
        """Simula resposta de compra de bilhetes."""
        resultado_turno = {
            "proximo_jogador": "player-3",
            "jogo_terminou": False,
            "mensagem_fim": None
        }
        
        response = ResponseBuilder.success_with_turn(
            message="João ficou com 2 bilhetes: Salvador → Recife, Brasília → Salvador",
            resultado_turno=resultado_turno,
            tickets_kept=2,
            tickets_returned=1
        )
        
        assert response["tickets_kept"] == 2
        assert response["tickets_returned"] == 1
    
    def test_cenario_ultima_rodada_ativada(self):
        """Simula última rodada sendo ativada."""
        resultado_turno = {
            "proximo_jogador": "player-1",
            "jogo_terminou": True,
            "mensagem_fim": "Última rodada! João tem 2 trens restantes."
        }
        
        response = ResponseBuilder.success_with_turn(
            message="Rota conquistada - última rodada ativada!",
            resultado_turno=resultado_turno,
            points=7,
            trains_remaining=2,
            game_ending=True
        )
        
        assert response["jogo_terminou"] is True
        assert "Última rodada" in response["mensagem_fim"]
        assert response["game_ending"] is True
    
    def test_cenario_passar_turno_manual(self):
        """Simula passagem de turno manual."""
        resultado_turno = {
            "proximo_jogador": "player-3",
            "jogo_terminou": False,
            "mensagem_fim": None
        }
        
        response = ResponseBuilder.success_with_turn(
            message="Turno passado para jogador player-3",
            resultado_turno=resultado_turno
        )
        
        assert "Turno passado" in response["message"]
        assert response["next_player"] == "player-3"
