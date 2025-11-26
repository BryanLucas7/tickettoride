"""
Testes para LocomotivaResetRule.

Testa a regra de negócio extraída do GerenciadorBaralhoVagoes.
"""

import pytest
from unittest.mock import MagicMock

from app.core.domain.rules import (
    LocomotivaResetRule,
    NullResetRule,
)
from app.core.domain.rules.locomotiva_reset_rule import CustomThresholdRule
from app.core.domain.entities.carta_vagao import CartaVagao
from app.core.domain.entities.cor import Cor


class TestLocomotivaResetRule:
    """Testes para LocomotivaResetRule."""
    
    @pytest.fixture
    def rule(self):
        """Fixture para criar a regra padrão."""
        return LocomotivaResetRule()
    
    @pytest.fixture
    def carta_normal(self):
        """Cria uma carta normal (não locomotiva)."""
        return CartaVagao(id=1, cor=Cor.AZUL, ehLocomotiva=False)
    
    @pytest.fixture
    def locomotiva(self):
        """Cria uma carta locomotiva."""
        return CartaVagao(id=100, cor=Cor.LOCOMOTIVA, ehLocomotiva=True)
    
    def test_deve_resetar_com_3_locomotivas(self, rule, carta_normal, locomotiva):
        """3 locomotivas deve retornar True."""
        cartas = [locomotiva, locomotiva, locomotiva, carta_normal, carta_normal]
        assert rule.deve_resetar(cartas) is True
    
    def test_deve_resetar_com_4_locomotivas(self, rule, locomotiva, carta_normal):
        """4 locomotivas deve retornar True."""
        cartas = [locomotiva, locomotiva, locomotiva, locomotiva, carta_normal]
        assert rule.deve_resetar(cartas) is True
    
    def test_deve_resetar_com_5_locomotivas(self, rule, locomotiva):
        """5 locomotivas deve retornar True."""
        cartas = [locomotiva] * 5
        assert rule.deve_resetar(cartas) is True
    
    def test_nao_deve_resetar_com_2_locomotivas(self, rule, carta_normal, locomotiva):
        """2 locomotivas deve retornar False."""
        cartas = [locomotiva, locomotiva, carta_normal, carta_normal, carta_normal]
        assert rule.deve_resetar(cartas) is False
    
    def test_nao_deve_resetar_com_1_locomotiva(self, rule, carta_normal, locomotiva):
        """1 locomotiva deve retornar False."""
        cartas = [locomotiva, carta_normal, carta_normal, carta_normal, carta_normal]
        assert rule.deve_resetar(cartas) is False
    
    def test_nao_deve_resetar_sem_locomotivas(self, rule, carta_normal):
        """0 locomotivas deve retornar False."""
        cartas = [carta_normal] * 5
        assert rule.deve_resetar(cartas) is False
    
    def test_nao_deve_resetar_lista_vazia(self, rule):
        """Lista vazia deve retornar False."""
        assert rule.deve_resetar([]) is False
    
    def test_obter_contagem_locomotivas(self, rule, locomotiva, carta_normal):
        """Deve contar corretamente o número de locomotivas."""
        cartas = [locomotiva, carta_normal, locomotiva, carta_normal, carta_normal]
        assert rule.obter_contagem_locomotivas(cartas) == 2
    
    def test_limite_locomotivas_eh_3(self, rule):
        """Verifica se o limite padrão é 3."""
        assert rule.LIMITE_LOCOMOTIVAS == 3


class TestNullResetRule:
    """Testes para NullResetRule."""
    
    @pytest.fixture
    def rule(self):
        return NullResetRule()
    
    def test_nunca_reseta_com_3_locomotivas(self, rule):
        """NullResetRule nunca deve resetar."""
        locomotiva = CartaVagao(id=1, cor=Cor.LOCOMOTIVA, ehLocomotiva=True)
        cartas = [locomotiva] * 5
        assert rule.deve_resetar(cartas) is False
    
    def test_nunca_reseta_lista_vazia(self, rule):
        """NullResetRule não reseta com lista vazia."""
        assert rule.deve_resetar([]) is False


class TestCustomThresholdRule:
    """Testes para CustomThresholdRule."""
    
    @pytest.fixture
    def locomotiva(self):
        return CartaVagao(id=1, cor=Cor.LOCOMOTIVA, ehLocomotiva=True)
    
    @pytest.fixture
    def carta_normal(self):
        return CartaVagao(id=2, cor=Cor.AZUL, ehLocomotiva=False)
    
    def test_limite_custom_2(self, locomotiva, carta_normal):
        """Teste com limite customizado de 2."""
        rule = CustomThresholdRule(limite=2)
        cartas_2_locos = [locomotiva, locomotiva, carta_normal, carta_normal, carta_normal]
        cartas_1_loco = [locomotiva, carta_normal, carta_normal, carta_normal, carta_normal]
        
        assert rule.deve_resetar(cartas_2_locos) is True
        assert rule.deve_resetar(cartas_1_loco) is False
    
    def test_limite_custom_4(self, locomotiva, carta_normal):
        """Teste com limite customizado de 4."""
        rule = CustomThresholdRule(limite=4)
        cartas_4_locos = [locomotiva] * 4 + [carta_normal]
        cartas_3_locos = [locomotiva] * 3 + [carta_normal] * 2
        
        assert rule.deve_resetar(cartas_4_locos) is True
        assert rule.deve_resetar(cartas_3_locos) is False
    
    def test_limite_default_3(self, locomotiva, carta_normal):
        """Limite padrão deve ser 3."""
        rule = CustomThresholdRule()
        assert rule.limite == 3


class TestCartasAbertasRuleProtocol:
    """Testes para verificar Protocol compliance."""
    
    def test_locomotiva_rule_implementa_protocol(self):
        """LocomotivaResetRule deve ser compatível com CartasAbertasRule."""
        from app.core.domain.rules import CartasAbertasRule
        rule = LocomotivaResetRule()
        assert isinstance(rule, CartasAbertasRule)
    
    def test_null_rule_implementa_protocol(self):
        """NullResetRule deve ser compatível com CartasAbertasRule."""
        from app.core.domain.rules import CartasAbertasRule
        rule = NullResetRule()
        assert isinstance(rule, CartasAbertasRule)
    
    def test_custom_rule_implementa_protocol(self):
        """CustomThresholdRule deve ser compatível com CartasAbertasRule."""
        from app.core.domain.rules import CartasAbertasRule
        rule = CustomThresholdRule()
        assert isinstance(rule, CartasAbertasRule)
