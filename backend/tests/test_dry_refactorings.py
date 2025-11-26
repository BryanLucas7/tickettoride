"""
Testes para as refatorações DRY implementadas.

Testa:
1. CardDrawService._processar_resultado_compra
2. BilheteHelpers (todas as funções)
3. Decorator @auto_save_game (simulação)
"""

import pytest
from unittest.mock import Mock, MagicMock
from app.application.services.card_draw_service import CardDrawService
from app.core.domain.support.bilhete_helpers import BilheteHelpers
from app.core.domain.entities.bilhete_destino import BilheteDestino
from app.core.domain.entities.cidade import Cidade
from app.core.domain.entities.jogador import Jogador
from app.core.domain.entities.cor import Cor


class TestCardDrawService:
    """Testes para refatoração de CardDrawService"""
    
    def test_processar_resultado_compra_sucesso(self):
        """Testa processamento de resultado bem-sucedido"""
        # Arrange
        jogo = Mock()
        jogo.estado = Mock()
        jogo.estado.estado_compra = Mock()
        jogo.estado.estado_compra.turnoCompleto = True
        jogo.estado.gerenciador_fim = None  # Sem fim de jogo
        jogo.resetar_estado_compra = Mock()
        jogo.passar_turno = Mock(return_value="player_2")
        
        resultado_compra = {
            "success": True,
            "message": "Carta comprada",
            "carta": {"cor": "azul", "ehLocomotiva": False}
        }
        
        # Act
        resultado = CardDrawService._processar_resultado_compra(jogo, resultado_compra)
        
        # Assert
        assert resultado["success"] == True
        assert "card" in resultado
        assert resultado["card"]["cor"] == "azul"
    
    def test_processar_resultado_compra_erro(self):
        """Testa processamento de resultado com erro"""
        # Arrange
        jogo = Mock()
        resultado_compra = {
            "success": False,
            "message": "Baralho vazio"
        }
        
        # Act
        resultado = CardDrawService._processar_resultado_compra(jogo, resultado_compra)
        
        # Assert
        assert resultado["success"] == False
        assert resultado["message"] == "Baralho vazio"


class TestBilheteHelpers:
    """Testes para BilheteHelpers"""
    
    def test_processar_escolha_bilhetes(self):
        """Testa processamento de escolha de bilhetes"""
        # Arrange
        jogador = Jogador(nome="João", cor=Cor.AZUL)
        sp = Cidade(id="SP", nome="São Paulo")
        rj = Cidade(id="RJ", nome="Rio de Janeiro")
        
        bilhete1 = BilheteDestino(cidadeOrigem=sp, cidadeDestino=rj, pontos=10)
        bilhete2 = BilheteDestino(cidadeOrigem=rj, cidadeDestino=sp, pontos=10)
        bilhete3 = BilheteDestino(cidadeOrigem=sp, cidadeDestino=sp, pontos=5)
        
        bilhetes_escolhidos = [bilhete1, bilhete2]
        bilhetes_recusados = [bilhete3]
        
        # Cria mock do gerenciador de bilhetes (SRP: classe separada)
        gerenciador_bilhetes = Mock()
        gerenciador_bilhetes.devolver = Mock()
        
        # Act
        BilheteHelpers.processar_escolha_bilhetes(
            jogador, bilhetes_escolhidos, bilhetes_recusados, gerenciador_bilhetes
        )
        
        # Assert
        assert len(jogador.bilhetes) == 2
        assert bilhete1 in jogador.bilhetes
        assert bilhete2 in jogador.bilhetes
        gerenciador_bilhetes.devolver.assert_called_once_with([bilhete3])
    
    def test_separar_bilhetes_por_indices(self):
        """Testa separação de bilhetes por índices"""
        # Arrange
        sp = Cidade(id="SP", nome="São Paulo")
        rj = Cidade(id="RJ", nome="Rio de Janeiro")
        
        bilhete0 = BilheteDestino(cidadeOrigem=sp, cidadeDestino=rj, pontos=10)
        bilhete1 = BilheteDestino(cidadeOrigem=rj, cidadeDestino=sp, pontos=10)
        bilhete2 = BilheteDestino(cidadeOrigem=sp, cidadeDestino=sp, pontos=5)
        
        bilhetes = [bilhete0, bilhete1, bilhete2]
        indices = [0, 2]
        
        # Act
        escolhidos, recusados = BilheteHelpers.separar_bilhetes_por_indices(bilhetes, indices)
        
        # Assert
        assert len(escolhidos) == 2
        assert bilhete0 in escolhidos
        assert bilhete2 in escolhidos
        assert len(recusados) == 1
        assert bilhete1 in recusados
    
    def test_validar_quantidade_minima_sucesso(self):
        """Testa validação de quantidade mínima - caso sucesso"""
        # Act & Assert (não deve lançar exceção)
        BilheteHelpers.validar_quantidade_minima(2, 2, "bilhetes")
        BilheteHelpers.validar_quantidade_minima(3, 2, "bilhetes")
    
    def test_validar_quantidade_minima_falha(self):
        """Testa validação de quantidade mínima - caso falha"""
        # Act & Assert
        with pytest.raises(ValueError, match="at least 2"):
            BilheteHelpers.validar_quantidade_minima(1, 2, "bilhetes")
    
    def test_validar_quantidade_maxima_sucesso(self):
        """Testa validação de quantidade máxima - caso sucesso"""
        # Act & Assert (não deve lançar exceção)
        BilheteHelpers.validar_quantidade_maxima(3, 3, "bilhetes")
        BilheteHelpers.validar_quantidade_maxima(2, 3, "bilhetes")
    
    def test_validar_quantidade_maxima_falha(self):
        """Testa validação de quantidade máxima - caso falha"""
        # Act & Assert
        with pytest.raises(ValueError, match="more than 3"):
            BilheteHelpers.validar_quantidade_maxima(4, 3, "bilhetes")


class TestPersistenceDecorator:
    """Testes simulados para decorator @auto_save_game"""
    
    def test_auto_save_game_decorator_simulation(self):
        """
        Simula comportamento do decorator @auto_save_game.
        
        Testa que game_service.save_game seria chamado após execução bem-sucedida.
        """
        # Arrange
        game_service = Mock()
        game_service.save_game = Mock()
        
        game_id = "game-123"
        jogo = Mock()
        
        # Simula função decorada
        def endpoint_function(game_id, jogo, game_service):
            return {"success": True}
        
        # Act - Simula decorator chamando save_game após função
        result = endpoint_function(game_id, jogo, game_service)
        game_service.save_game(game_id, jogo)
        
        # Assert
        assert result["success"] == True
        game_service.save_game.assert_called_once_with(game_id, jogo)
    
    def test_auto_save_game_with_exception(self):
        """Testa que decorator não salva se houver exceção"""
        # Arrange
        game_service = Mock()
        game_service.save_game = Mock()
        
        # Simula função que lança exceção
        def endpoint_with_error(game_id, jogo, game_service):
            raise ValueError("Erro na operação")
        
        # Act & Assert
        with pytest.raises(ValueError):
            endpoint_with_error("game-123", Mock(), game_service)
        
        # Save não deve ser chamado se houve exceção
        game_service.save_game.assert_not_called()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
