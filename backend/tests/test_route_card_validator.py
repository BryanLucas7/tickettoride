"""
Testes para RouteCardValidator.

Verifica todas as regras de validação de cartas para conquista de rotas.
"""

import pytest
from unittest.mock import Mock, MagicMock

from app.core.domain.validators.route_card_validator import (
    RouteCardValidator, 
    CardValidationResult
)
from app.core.domain.entities.cor import Cor


class TestRouteCardValidator:
    """Testes para RouteCardValidator."""
    
    @pytest.fixture
    def validator(self):
        """Fixture que retorna instância do validator."""
        return RouteCardValidator()
    
    @pytest.fixture
    def rota_azul(self):
        """Fixture para rota azul de comprimento 3."""
        rota = Mock()
        rota.cor = Cor.AZUL
        rota.comprimento = 3
        return rota
    
    @pytest.fixture
    def rota_cinza(self):
        """Fixture para rota cinza de comprimento 2."""
        rota = Mock()
        rota.cor = Cor.CINZA
        rota.comprimento = 2
        return rota
    
    def _criar_carta(self, cor: Cor, eh_locomotiva: bool = False):
        """Helper para criar carta mock."""
        carta = Mock()
        carta.cor = cor
        carta.ehLocomotiva = eh_locomotiva
        return carta
    
    # === Testes de Quantidade ===
    
    def test_validar_quantidade_correta(self, validator, rota_azul):
        """Deve passar quando quantidade de cartas é correta."""
        cartas = [
            self._criar_carta(Cor.AZUL),
            self._criar_carta(Cor.AZUL),
            self._criar_carta(Cor.AZUL),
        ]
        
        resultado = validator.validar(rota_azul, cartas)
        
        assert resultado.valido is True
        assert resultado.erro is None
    
    def test_validar_quantidade_insuficiente(self, validator, rota_azul):
        """Deve falhar quando há menos cartas que o necessário."""
        cartas = [
            self._criar_carta(Cor.AZUL),
            self._criar_carta(Cor.AZUL),
        ]
        
        resultado = validator.validar(rota_azul, cartas)
        
        assert resultado.valido is False
        assert "exatamente 3 carta(s)" in resultado.erro
    
    def test_validar_quantidade_excedente(self, validator, rota_azul):
        """Deve falhar quando há mais cartas que o necessário."""
        cartas = [
            self._criar_carta(Cor.AZUL),
            self._criar_carta(Cor.AZUL),
            self._criar_carta(Cor.AZUL),
            self._criar_carta(Cor.AZUL),
        ]
        
        resultado = validator.validar(rota_azul, cartas)
        
        assert resultado.valido is False
        assert "exatamente 3 carta(s)" in resultado.erro
    
    # === Testes de Rota Colorida ===
    
    def test_validar_rota_colorida_cartas_corretas(self, validator, rota_azul):
        """Deve passar com cartas da cor correta."""
        cartas = [
            self._criar_carta(Cor.AZUL),
            self._criar_carta(Cor.AZUL),
            self._criar_carta(Cor.AZUL),
        ]
        
        resultado = validator.validar(rota_azul, cartas)
        
        assert resultado.valido is True
    
    def test_validar_rota_colorida_com_locomotivas(self, validator, rota_azul):
        """Deve passar com mix de cartas da cor e locomotivas."""
        cartas = [
            self._criar_carta(Cor.AZUL),
            self._criar_carta(Cor.LOCOMOTIVA, eh_locomotiva=True),
            self._criar_carta(Cor.AZUL),
        ]
        
        resultado = validator.validar(rota_azul, cartas)
        
        assert resultado.valido is True
    
    def test_validar_rota_colorida_apenas_locomotivas(self, validator, rota_azul):
        """Deve passar com apenas locomotivas."""
        cartas = [
            self._criar_carta(Cor.LOCOMOTIVA, eh_locomotiva=True),
            self._criar_carta(Cor.LOCOMOTIVA, eh_locomotiva=True),
            self._criar_carta(Cor.LOCOMOTIVA, eh_locomotiva=True),
        ]
        
        resultado = validator.validar(rota_azul, cartas)
        
        assert resultado.valido is True
    
    def test_validar_rota_colorida_cor_errada(self, validator, rota_azul):
        """Deve falhar com cartas de cor errada."""
        cartas = [
            self._criar_carta(Cor.VERMELHO),
            self._criar_carta(Cor.AZUL),
            self._criar_carta(Cor.AZUL),
        ]
        
        resultado = validator.validar(rota_azul, cartas)
        
        assert resultado.valido is False
        assert "AZUL" in resultado.erro or "azul" in resultado.erro.lower()
    
    # === Testes de Rota Cinza ===
    
    def test_validar_rota_cinza_mesma_cor(self, validator, rota_cinza):
        """Deve passar com cartas da mesma cor (qualquer cor)."""
        cartas = [
            self._criar_carta(Cor.VERDE),
            self._criar_carta(Cor.VERDE),
        ]
        
        resultado = validator.validar(rota_cinza, cartas)
        
        assert resultado.valido is True
    
    def test_validar_rota_cinza_com_locomotivas(self, validator, rota_cinza):
        """Deve passar com mix de cor e locomotivas."""
        cartas = [
            self._criar_carta(Cor.VERDE),
            self._criar_carta(Cor.LOCOMOTIVA, eh_locomotiva=True),
        ]
        
        resultado = validator.validar(rota_cinza, cartas)
        
        assert resultado.valido is True
    
    def test_validar_rota_cinza_cores_diferentes(self, validator, rota_cinza):
        """Deve falhar com cartas de cores diferentes."""
        cartas = [
            self._criar_carta(Cor.VERDE),
            self._criar_carta(Cor.VERMELHO),
        ]
        
        resultado = validator.validar(rota_cinza, cartas)
        
        assert resultado.valido is False
        assert "mesma cor" in resultado.erro.lower()
    
    # === Teste de Propriedade invalido ===
    
    def test_propriedade_invalido(self, validator, rota_azul):
        """Deve retornar True para invalido quando falhar."""
        cartas = [self._criar_carta(Cor.AZUL)]  # Quantidade errada
        
        resultado = validator.validar(rota_azul, cartas)
        
        assert resultado.invalido is True
        assert resultado.valido is False
