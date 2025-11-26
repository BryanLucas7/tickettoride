"""
Testes para validators de compra refatorados.

Testa a separação de responsabilidades do CompraValidator original
em validators específicos: JogadorValidator, CartaFechadaValidator, CartaAbertaValidator.
"""

import pytest
from unittest.mock import MagicMock, PropertyMock

from app.core.domain.validators.compra import (
    JogadorValidator,
    JogadorValidationResult,
    CartaFechadaValidator,
    CompraFechadaValidationResult,
    CartaAbertaValidator,
    CompraAbertaValidationResult,
    CompraValidator,
    CompraValidationResult
)
from app.core.domain.entities.carta_vagao import CartaVagao
from app.core.domain.entities.cor import Cor


class TestJogadorValidator:
    """Testes para JogadorValidator."""
    
    @pytest.fixture
    def mock_gerenciador_turnos(self):
        """Mock do gerenciador de turnos."""
        return MagicMock()
    
    @pytest.fixture
    def validator(self, mock_gerenciador_turnos):
        """Validator com mock injetado."""
        return JogadorValidator(mock_gerenciador_turnos)
    
    def test_validar_jogador_existente(self, validator, mock_gerenciador_turnos):
        """Deve retornar válido para jogador existente."""
        jogador_mock = MagicMock()
        jogador_mock.id = "jogador-123"
        mock_gerenciador_turnos.obter_jogador_por_id.return_value = jogador_mock
        
        resultado = validator.validar("jogador-123")
        
        assert resultado.valido is True
        assert resultado.jogador == jogador_mock
        assert resultado.erro is None
    
    def test_validar_jogador_inexistente(self, validator, mock_gerenciador_turnos):
        """Deve retornar inválido para jogador não encontrado."""
        mock_gerenciador_turnos.obter_jogador_por_id.return_value = None
        
        resultado = validator.validar("jogador-inexistente")
        
        assert resultado.valido is False
        assert resultado.invalido is True
        assert "não encontrado" in resultado.erro
        assert resultado.jogador is None
    
    def test_validar_id_vazio(self, validator):
        """Deve retornar inválido para ID vazio."""
        resultado = validator.validar("")
        
        assert resultado.valido is False
        assert "não fornecido" in resultado.erro
    
    def test_validar_jogador_atual_correto(self, validator, mock_gerenciador_turnos):
        """Deve validar se é o jogador do turno atual."""
        jogador_mock = MagicMock()
        jogador_mock.id = "jogador-123"
        mock_gerenciador_turnos.obter_jogador_por_id.return_value = jogador_mock
        mock_gerenciador_turnos.jogadorAtual = jogador_mock
        
        resultado = validator.validar_jogador_atual("jogador-123")
        
        assert resultado.valido is True
    
    def test_validar_jogador_atual_errado(self, validator, mock_gerenciador_turnos):
        """Deve falhar se não é o turno do jogador."""
        jogador_mock = MagicMock()
        jogador_mock.id = "jogador-123"
        outro_jogador = MagicMock()
        outro_jogador.id = "outro-jogador"
        outro_jogador.nome = "Outro"
        
        mock_gerenciador_turnos.obter_jogador_por_id.return_value = jogador_mock
        mock_gerenciador_turnos.jogadorAtual = outro_jogador
        
        resultado = validator.validar_jogador_atual("jogador-123")
        
        assert resultado.valido is False
        assert "Não é o turno" in resultado.erro


class TestCartaFechadaValidator:
    """Testes para CartaFechadaValidator."""
    
    @pytest.fixture
    def mock_estado_compra(self):
        return MagicMock()
    
    @pytest.fixture
    def mock_gerenciador_baralho(self):
        return MagicMock()
    
    @pytest.fixture
    def validator(self, mock_estado_compra, mock_gerenciador_baralho):
        return CartaFechadaValidator(mock_estado_compra, mock_gerenciador_baralho)
    
    def test_validar_compra_permitida(self, validator, mock_estado_compra, mock_gerenciador_baralho):
        """Deve permitir compra quando estado e baralho OK."""
        mock_estado_compra.podeComprarCartaFechada.return_value = True
        mock_gerenciador_baralho.baralhoVagoes.cartas = [MagicMock()]  # Tem cartas
        
        resultado = validator.validar()
        
        assert resultado.valido is True
    
    def test_validar_compra_bloqueada_por_estado(self, validator, mock_estado_compra):
        """Deve bloquear quando estado não permite."""
        mock_estado_compra.podeComprarCartaFechada.return_value = False
        mock_estado_compra.obterMensagemStatus.return_value = "Já comprou locomotiva"
        
        resultado = validator.validar()
        
        assert resultado.valido is False
        assert "locomotiva" in resultado.erro.lower()
    
    def test_validar_baralho_vazio_sem_descarte(self, validator, mock_estado_compra, mock_gerenciador_baralho):
        """Deve falhar quando baralho vazio e sem descarte."""
        mock_estado_compra.podeComprarCartaFechada.return_value = True
        mock_gerenciador_baralho.baralhoVagoes.cartas = []
        mock_gerenciador_baralho.descarteVagoes = []
        
        resultado = validator.validar()
        
        assert resultado.valido is False
        assert "vazio" in resultado.erro.lower()
    
    def test_validar_baralho_vazio_com_descarte(self, validator, mock_estado_compra, mock_gerenciador_baralho):
        """Deve permitir quando baralho vazio mas tem descarte."""
        mock_estado_compra.podeComprarCartaFechada.return_value = True
        mock_gerenciador_baralho.baralhoVagoes.cartas = []
        mock_gerenciador_baralho.descarteVagoes = [MagicMock()]
        
        resultado = validator.validar()
        
        assert resultado.valido is True


class TestCartaAbertaValidator:
    """Testes para CartaAbertaValidator."""
    
    @pytest.fixture
    def mock_estado_compra(self):
        return MagicMock()
    
    @pytest.fixture
    def mock_gerenciador_baralho(self):
        return MagicMock()
    
    @pytest.fixture
    def validator(self, mock_estado_compra, mock_gerenciador_baralho):
        return CartaAbertaValidator(mock_estado_compra, mock_gerenciador_baralho)
    
    @pytest.fixture
    def cartas_abertas(self):
        """5 cartas abertas de teste."""
        return [
            CartaVagao(id=i, cor=Cor.AZUL, ehLocomotiva=False)
            for i in range(5)
        ]
    
    def test_validar_indice_valido(self, validator, mock_gerenciador_baralho, cartas_abertas, mock_estado_compra):
        """Deve aceitar índice válido (0-4)."""
        mock_gerenciador_baralho.obterCartasAbertas.return_value = cartas_abertas
        mock_estado_compra.podeComprarCartaAberta.return_value = True
        
        resultado = validator.validar(2)
        
        assert resultado.valido is True
        assert resultado.carta is not None
    
    def test_validar_indice_negativo(self, validator, mock_gerenciador_baralho, cartas_abertas):
        """Deve rejeitar índice negativo."""
        mock_gerenciador_baralho.obterCartasAbertas.return_value = cartas_abertas
        
        resultado = validator.validar(-1)
        
        assert resultado.valido is False
        assert "-1" in resultado.erro
    
    def test_validar_indice_muito_grande(self, validator, mock_gerenciador_baralho, cartas_abertas):
        """Deve rejeitar índice >= 5."""
        mock_gerenciador_baralho.obterCartasAbertas.return_value = cartas_abertas
        
        resultado = validator.validar(5)
        
        assert resultado.valido is False
        assert "5" in resultado.erro
    
    def test_validar_locomotiva_primeira_carta(self, validator, mock_gerenciador_baralho, mock_estado_compra):
        """Deve permitir locomotiva como primeira carta."""
        locomotiva = CartaVagao(id=1, cor=Cor.LOCOMOTIVA, ehLocomotiva=True)
        cartas = [locomotiva] + [CartaVagao(id=i, cor=Cor.AZUL, ehLocomotiva=False) for i in range(2, 6)]
        
        mock_gerenciador_baralho.obterCartasAbertas.return_value = cartas
        mock_estado_compra.podeComprarCartaAberta.return_value = True
        
        resultado = validator.validar(0)
        
        assert resultado.valido is True
    
    def test_validar_locomotiva_segunda_carta_bloqueada(self, validator, mock_gerenciador_baralho, mock_estado_compra):
        """Deve bloquear locomotiva como segunda carta."""
        locomotiva = CartaVagao(id=1, cor=Cor.LOCOMOTIVA, ehLocomotiva=True)
        cartas = [locomotiva] + [CartaVagao(id=i, cor=Cor.AZUL, ehLocomotiva=False) for i in range(2, 6)]
        
        mock_gerenciador_baralho.obterCartasAbertas.return_value = cartas
        mock_estado_compra.podeComprarCartaAberta.return_value = False
        mock_estado_compra.obterMensagemStatus.return_value = "Não pode comprar locomotiva"
        
        resultado = validator.validar(0)
        
        assert resultado.valido is False


class TestCompraValidatorComposite:
    """Testes para CompraValidator (Composite)."""
    
    @pytest.fixture
    def mock_jogo(self):
        """Mock completo do jogo."""
        jogo = MagicMock()
        
        # Estado
        jogo.estado.estado_compra.podeComprarCartaFechada.return_value = True
        jogo.estado.estado_compra.podeComprarCartaAberta.return_value = True
        jogo.estado.estado_compra.turnoCompleto = False
        jogo.estado.estado_compra.obterMensagemStatus.return_value = ""
        
        # Gerenciador de turnos
        jogador = MagicMock()
        jogador.id = "jogador-1"
        jogo.gerenciadorDeTurnos.obter_jogador_por_id.return_value = jogador
        
        # Gerenciador de baralho
        cartas = [CartaVagao(id=i, cor=Cor.AZUL, ehLocomotiva=False) for i in range(5)]
        jogo.gerenciadorDeBaralhoVagoes.obterCartasAbertas.return_value = cartas
        jogo.gerenciadorDeBaralhoVagoes.baralhoVagoes.cartas = [MagicMock()]
        jogo.gerenciadorDeBaralhoVagoes.descarteVagoes = []
        
        return jogo
    
    @pytest.fixture
    def validator(self, mock_jogo):
        return CompraValidator(mock_jogo)
    
    def test_validar_jogador_delegado(self, validator, mock_jogo):
        """Deve delegar validação de jogador para JogadorValidator."""
        resultado = validator.validar_jogador("jogador-1")
        
        mock_jogo.gerenciadorDeTurnos.obter_jogador_por_id.assert_called_once()
        assert resultado.valido is True
    
    def test_validar_compra_fechada_completa(self, validator):
        """Deve validar compra fechada completa."""
        resultado = validator.validar_compra_carta_fechada_completa("jogador-1")
        
        assert resultado.valido is True
        assert resultado.jogador is not None
    
    def test_validar_compra_aberta_completa(self, validator):
        """Deve validar compra aberta completa."""
        resultado, carta = validator.validar_compra_carta_aberta_completa("jogador-1", 2)
        
        assert resultado.valido is True
        assert carta is not None
    
    def test_ha_opcao_de_compra_true(self, validator):
        """Deve retornar True quando há opções."""
        resultado = validator.ha_opcao_de_compra()
        
        assert resultado is True
    
    def test_ha_opcao_de_compra_turno_completo(self, validator, mock_jogo):
        """Deve retornar False quando turno completo."""
        mock_jogo.estado.estado_compra.turnoCompleto = True
        
        resultado = validator.ha_opcao_de_compra()
        
        assert resultado is False


class TestCompraValidationResultConversions:
    """Testes para conversões de resultado."""
    
    def test_from_jogador_result_valido(self):
        """Deve converter JogadorValidationResult válido."""
        jogador = MagicMock()
        original = JogadorValidationResult(valido=True, jogador=jogador)
        
        convertido = CompraValidationResult.from_jogador_result(original)
        
        assert convertido.valido is True
        assert convertido.jogador == jogador
    
    def test_from_fechada_result_invalido(self):
        """Deve converter CompraFechadaValidationResult inválido."""
        original = CompraFechadaValidationResult(valido=False, erro="Baralho vazio")
        
        convertido = CompraValidationResult.from_fechada_result(original)
        
        assert convertido.valido is False
        assert convertido.erro == "Baralho vazio"
    
    def test_from_aberta_result_valido(self):
        """Deve converter CompraAbertaValidationResult válido."""
        carta = CartaVagao(id=1, cor=Cor.AZUL, ehLocomotiva=False)
        original = CompraAbertaValidationResult(valido=True, carta=carta)
        
        convertido = CompraValidationResult.from_aberta_result(original)
        
        assert convertido.valido is True
