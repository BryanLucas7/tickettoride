"""
Testes para o sistema de eventos de conquista.

Verifica:
- ConquestEventPublisher: subscribe/unsubscribe/publish
- ScoreObserver: registro de pontos
- GameEndObserver: verificação de fim de jogo
"""

import pytest
from unittest.mock import Mock, MagicMock, patch

from app.core.domain.events import (
    ConquestEvent, 
    ConquestObserver, 
    ConquestEventPublisher
)
from app.core.domain.events.conquest_observers import (
    ScoreObserver, 
    GameEndObserver,
    LoggingObserver
)
from app.core.domain.entities.cor import Cor


class TestConquestEvent:
    """Testes para ConquestEvent."""
    
    @pytest.fixture
    def jogador_mock(self):
        """Fixture para jogador mock."""
        jogador = Mock()
        jogador.id = "jogador-1"
        jogador.nome = "Alice"
        return jogador
    
    @pytest.fixture
    def rota_mock(self):
        """Fixture para rota mock."""
        rota = Mock()
        rota.id = "rota-1"
        rota.cidadeA = Mock()
        rota.cidadeA.nome = "São Paulo"
        rota.cidadeB = Mock()
        rota.cidadeB.nome = "Rio de Janeiro"
        rota.comprimento = 3
        return rota
    
    def test_criar_evento(self, jogador_mock, rota_mock):
        """Deve criar evento com dados corretos."""
        evento = ConquestEvent(
            jogador=jogador_mock,
            rota=rota_mock,
            pontos_ganhos=4,
            trens_restantes=42
        )
        
        assert evento.jogador == jogador_mock
        assert evento.rota == rota_mock
        assert evento.pontos_ganhos == 4
        assert evento.trens_restantes == 42
    
    def test_nome_rota(self, jogador_mock, rota_mock):
        """Deve formatar nome da rota corretamente."""
        evento = ConquestEvent(
            jogador=jogador_mock,
            rota=rota_mock,
            pontos_ganhos=4,
            trens_restantes=42
        )
        
        assert evento.nome_rota == "São Paulo → Rio de Janeiro"


class TestConquestEventPublisher:
    """Testes para ConquestEventPublisher."""
    
    @pytest.fixture
    def publisher(self):
        """Fixture para publisher."""
        return ConquestEventPublisher()
    
    @pytest.fixture
    def observer_mock(self):
        """Fixture para observer mock."""
        observer = Mock(spec=ConquestObserver)
        return observer
    
    @pytest.fixture
    def evento_mock(self):
        """Fixture para evento mock."""
        return Mock(spec=ConquestEvent)
    
    def test_subscribe_observer(self, publisher, observer_mock):
        """Deve registrar observer."""
        publisher.subscribe(observer_mock)
        
        assert publisher.observer_count == 1
    
    def test_subscribe_mesmo_observer_duas_vezes(self, publisher, observer_mock):
        """Não deve duplicar observer."""
        publisher.subscribe(observer_mock)
        publisher.subscribe(observer_mock)
        
        assert publisher.observer_count == 1
    
    def test_unsubscribe_observer(self, publisher, observer_mock):
        """Deve remover observer."""
        publisher.subscribe(observer_mock)
        publisher.unsubscribe(observer_mock)
        
        assert publisher.observer_count == 0
    
    def test_publish_notifica_observers(self, publisher, observer_mock, evento_mock):
        """Deve notificar todos os observers."""
        observer2 = Mock(spec=ConquestObserver)
        
        publisher.subscribe(observer_mock)
        publisher.subscribe(observer2)
        publisher.publish(evento_mock)
        
        observer_mock.on_conquest.assert_called_once_with(evento_mock)
        observer2.on_conquest.assert_called_once_with(evento_mock)
    
    def test_publish_sem_observers(self, publisher, evento_mock):
        """Deve funcionar sem observers (não lança exceção)."""
        publisher.publish(evento_mock)  # Não deve lançar exceção
    
    def test_clear(self, publisher, observer_mock):
        """Deve limpar todos os observers."""
        publisher.subscribe(observer_mock)
        publisher.clear()
        
        assert publisher.observer_count == 0


class TestScoreObserver:
    """Testes para ScoreObserver."""
    
    @pytest.fixture
    def placar_mock(self):
        """Fixture para placar mock."""
        return Mock()
    
    @pytest.fixture
    def evento_mock(self):
        """Fixture para evento de conquista mock."""
        evento = Mock(spec=ConquestEvent)
        evento.jogador = Mock()
        evento.jogador.id = "jogador-1"
        evento.jogador.nome = "Alice"
        evento.rota = Mock()
        evento.rota.comprimento = 3
        evento.nome_rota = "São Paulo → Rio de Janeiro"
        evento.pontos_ganhos = 4
        return evento
    
    def test_on_conquest_registra_pontos(self, placar_mock, evento_mock):
        """Deve registrar pontos no placar."""
        observer = ScoreObserver(placar_mock)
        
        observer.on_conquest(evento_mock)
        
        placar_mock.adicionar_pontos_rota.assert_called_once_with(
            jogador_id="jogador-1",
            comprimento_rota=3,
            nome_rota="São Paulo → Rio de Janeiro"
        )
    
    def test_on_conquest_placar_none(self, evento_mock):
        """Deve ignorar se placar é None."""
        observer = ScoreObserver(None)
        
        # Não deve lançar exceção
        observer.on_conquest(evento_mock)


class TestGameEndObserver:
    """Testes para GameEndObserver."""
    
    @pytest.fixture
    def gerenciador_mock(self):
        """Fixture para gerenciador de fim mock."""
        return Mock()
    
    @pytest.fixture
    def evento_mock(self):
        """Fixture para evento de conquista mock."""
        evento = Mock(spec=ConquestEvent)
        evento.jogador = Mock()
        evento.jogador.id = "jogador-1"
        evento.trens_restantes = 2
        return evento
    
    def test_on_conquest_fim_ativado(self, gerenciador_mock, evento_mock):
        """Deve detectar fim de jogo quando ativado."""
        gerenciador_mock.verificar_condicao_fim.return_value = {
            "fim_ativado": True,
            "mensagem": "Jogador com 2 ou menos trens!"
        }
        observer = GameEndObserver(gerenciador_mock)
        
        observer.on_conquest(evento_mock)
        
        assert observer.fim_ativado is True
        assert observer.mensagem_fim == "Jogador com 2 ou menos trens!"
    
    def test_on_conquest_fim_nao_ativado(self, gerenciador_mock, evento_mock):
        """Deve não ativar fim quando condição não atendida."""
        gerenciador_mock.verificar_condicao_fim.return_value = {
            "fim_ativado": False,
            "mensagem": None
        }
        observer = GameEndObserver(gerenciador_mock)
        
        observer.on_conquest(evento_mock)
        
        assert observer.fim_ativado is False
        assert observer.mensagem_fim is None
    
    def test_on_conquest_gerenciador_none(self, evento_mock):
        """Deve ignorar se gerenciador é None."""
        observer = GameEndObserver(None)
        
        # Não deve lançar exceção
        observer.on_conquest(evento_mock)
        
        assert observer.fim_ativado is False
    
    def test_reset(self, gerenciador_mock, evento_mock):
        """Deve resetar estado corretamente."""
        gerenciador_mock.verificar_condicao_fim.return_value = {
            "fim_ativado": True,
            "mensagem": "Fim!"
        }
        observer = GameEndObserver(gerenciador_mock)
        observer.on_conquest(evento_mock)
        
        observer.reset()
        
        assert observer.fim_ativado is False
        assert observer.mensagem_fim is None


class TestLoggingObserver:
    """Testes para LoggingObserver."""
    
    @pytest.fixture
    def evento_mock(self):
        """Fixture para evento de conquista mock."""
        evento = Mock(spec=ConquestEvent)
        evento.jogador = Mock()
        evento.jogador.nome = "Alice"
        evento.nome_rota = "São Paulo → Rio de Janeiro"
        evento.pontos_ganhos = 4
        evento.trens_restantes = 42
        return evento
    
    @patch('app.core.domain.events.conquest_observers.logger')
    def test_on_conquest_loga_info(self, logger_mock, evento_mock):
        """Deve registrar log da conquista."""
        import logging
        observer = LoggingObserver(log_level=logging.INFO)
        
        observer.on_conquest(evento_mock)
        
        logger_mock.log.assert_called_once()
        call_args = logger_mock.log.call_args
        assert call_args[0][0] == logging.INFO
        assert "Alice" in call_args[0][1]
        assert "São Paulo → Rio de Janeiro" in call_args[0][1]
