"""
Testes para EntityFormatters.formatar_carta

Valida formatação para CartaVagao.
"""

import pytest
import sys
from pathlib import Path

# Adiciona o diretório do backend ao path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from app.shared.formatters import EntityFormatters
from app.core.domain.entities.cor import Cor


# Mock de CartaVagao para evitar imports circulares
class MockCartaVagao:
    """Mock simplificado de CartaVagao para testes."""
    def __init__(self, cor, ehLocomotiva):
        self.cor = cor
        self.ehLocomotiva = ehLocomotiva


class TestFormatarCartaUnificado:
    """Testes para EntityFormatters.formatar_carta() com CartaVagao."""
    
    def test_formatar_carta_com_cartavagao(self):
        """Deve formatar CartaVagao corretamente."""
        carta = MockCartaVagao(cor=Cor.VERMELHO, ehLocomotiva=False)
        
        resultado = EntityFormatters.formatar_carta(carta)
        
        assert resultado["cor"] == "vermelho"
        assert resultado["eh_locomotiva"] is False
    
    def test_formatar_carta_com_locomotiva(self):
        """Deve formatar locomotiva corretamente."""
        carta = MockCartaVagao(cor=Cor.LOCOMOTIVA, ehLocomotiva=True)
        
        resultado = EntityFormatters.formatar_carta(carta)
        
        assert resultado["cor"] == "locomotiva"
        assert resultado["eh_locomotiva"] is True
    
    def test_formatar_carta_todas_as_cores(self):
        """Deve formatar todas as cores corretamente."""
        cores = [
            (Cor.VERMELHO, "vermelho"),
            (Cor.AZUL, "azul"),
            (Cor.VERDE, "verde"),
            (Cor.AMARELO, "amarelo"),
            (Cor.LARANJA, "laranja"),
            (Cor.BRANCO, "branco"),
            (Cor.PRETO, "preto"),
            (Cor.ROXO, "roxo"),
            (Cor.LOCOMOTIVA, "locomotiva"),
            (Cor.CINZA, "cinza")
        ]
        
        for cor_enum, cor_string in cores:
            carta = MockCartaVagao(cor=cor_enum, ehLocomotiva=False)
            resultado = EntityFormatters.formatar_carta(carta)
            assert resultado["cor"] == cor_string
    
    def test_formatar_cartas_lista_cartavagao(self):
        """Deve formatar lista de CartaVagao."""
        cartas = [
            MockCartaVagao(cor=Cor.VERMELHO, ehLocomotiva=False),
            MockCartaVagao(cor=Cor.AZUL, ehLocomotiva=False),
            MockCartaVagao(cor=Cor.LOCOMOTIVA, ehLocomotiva=True)
        ]
        
        resultado = EntityFormatters.formatar_cartas(cartas)
        
        assert len(resultado) == 3
        assert resultado[0]["cor"] == "vermelho"
        assert resultado[1]["cor"] == "azul"
        assert resultado[2]["cor"] == "locomotiva"
        assert resultado[2]["eh_locomotiva"] is True
    
    def test_formatar_cartas_lista_vazia(self):
        """Deve lidar com lista vazia."""
        resultado = EntityFormatters.formatar_cartas([])
        
        assert resultado == []
        assert isinstance(resultado, list)

