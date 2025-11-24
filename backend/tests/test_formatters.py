"""
Testes para EntityFormatters e ResponseAssembler

Garante formatação consistente e correta de entidades do domínio.
"""

import pytest
import sys
from pathlib import Path

# Adicionar diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from app.shared.formatters import EntityFormatters
from app.shared.response_assembler import ResponseAssembler
from app.core.domain.entities.carta_vagao import CartaVagao
from app.core.domain.entities.cor import Cor
from app.core.domain.entities.bilhete_destino import BilheteDestino
from app.core.domain.entities.cidade import Cidade, CIDADES, get_cidade
from app.core.domain.entities.rota import Rota
from app.core.domain.entities.jogador import Jogador


class TestEntityFormatters:
    """Testes para EntityFormatters"""
    
    def test_formatar_carta_objeto(self):
        """Testa formatação de CartaVagao (objeto)"""
        carta = CartaVagao(cor=Cor.VERMELHO, ehLocomotiva=False)
        resultado = EntityFormatters.formatar_carta(carta)
        
        assert resultado == {
            "cor": "vermelho",
            "eh_locomotiva": False
        }
    
    def test_formatar_cartas_lista(self):
        """Testa formatação de lista de cartas"""
        cartas = [
            CartaVagao(cor=Cor.AZUL, ehLocomotiva=False),
            CartaVagao(cor=Cor.VERDE, ehLocomotiva=True)
        ]
        resultado = EntityFormatters.formatar_cartas(cartas)
        
        assert len(resultado) == 2
        assert resultado[0]["cor"] == "azul"
        assert resultado[1]["eh_locomotiva"] is True
    
    def test_formatar_bilhete_padrao(self):
        """Testa formatação padrão de bilhete"""
        origem = get_cidade("RIO_DE_JANEIRO")
        destino = get_cidade("PORTO_ALEGRE")
        bilhete = BilheteDestino(cidadeOrigem=origem, cidadeDestino=destino, pontos=10)
        
        resultado = EntityFormatters.formatar_bilhete(bilhete, completo=True, formato="padrao")
        
        assert resultado["cidadeOrigem"] == "Rio de Janeiro"
        assert resultado["cidadeDestino"] == "Porto Alegre"
        assert resultado["pontos"] == 10
        assert resultado["completo"] is True
        assert "id" in resultado
    
    def test_formatar_bilhete_compacto(self):
        """Testa formatação compacta de bilhete (sem ID, sem completo)"""
        origem = get_cidade("RIO_DE_JANEIRO")
        destino = get_cidade("SALVADOR")
        bilhete = BilheteDestino(cidadeOrigem=origem, cidadeDestino=destino, pontos=10)
        
        resultado = EntityFormatters.formatar_bilhete(bilhete, formato="compacto")
        
        assert resultado == {
            "origem": "Rio de Janeiro",
            "destino": "Salvador",
            "pontos": 10
        }
        assert "completo" not in resultado
        assert "id" not in resultado
    
    def test_formatar_bilhete_origem_destino(self):
        """Testa formatação origem_destino de bilhete"""
        origem = get_cidade("BRASILIA")
        destino = get_cidade("SALVADOR")
        bilhete = BilheteDestino(cidadeOrigem=origem, cidadeDestino=destino, pontos=15)
        
        resultado = EntityFormatters.formatar_bilhete(bilhete, completo=False, formato="origem_destino")
        
        assert resultado == {
            "origem": "Brasília",
            "destino": "Salvador",
            "pontos": 15,
            "completo": False
        }
    
    def test_formatar_rotas_bilhetes_vazio(self):
        """Testa formatação de lista vazia de bilhetes"""
        resultado = EntityFormatters.formatar_rotas_bilhetes([])
        assert resultado == ""
    
    def test_formatar_rotas_bilhetes_multiplos(self):
        """Testa formatação de múltiplos bilhetes como texto"""
        origem1 = get_cidade("RIO_DE_JANEIRO")
        destino1 = get_cidade("PORTO_ALEGRE")
        bilhete1 = BilheteDestino(cidadeOrigem=origem1, cidadeDestino=destino1, pontos=10)
        
        origem2 = get_cidade("BRASILIA")
        destino2 = get_cidade("SALVADOR")
        bilhete2 = BilheteDestino(cidadeOrigem=origem2, cidadeDestino=destino2, pontos=12)
        
        resultado = EntityFormatters.formatar_rotas_bilhetes([bilhete1, bilhete2])
        
        assert "Rio de Janeiro → Porto Alegre" in resultado
        assert "Brasília → Salvador" in resultado
        assert ", " in resultado
    
    def test_criar_mensagem_compra_bilhetes(self):
        """Testa criação de mensagem de compra de bilhetes"""
        origem = get_cidade("RIO_DE_JANEIRO")
        destino = get_cidade("SALVADOR")
        bilhete = BilheteDestino(cidadeOrigem=origem, cidadeDestino=destino, pontos=10)
        
        resultado = EntityFormatters.criar_mensagem_compra_bilhetes(
            jogador_nome="João",
            bilhetes_escolhidos=[bilhete],
            quantidade_recusados=2
        )
        
        assert "João" in resultado
        assert "ficou com 1 bilhete(s)" in resultado
        assert "devolveu 2" in resultado
        assert "Rio de Janeiro → Salvador" in resultado
    
    def test_formatar_jogador_basico(self):
        """Testa formatação básica de jogador (sem cartas/bilhetes)"""
        jogador = Jogador(id="1", nome="Alice", cor=Cor.VERMELHO)
        
        resultado = EntityFormatters.formatar_jogador(jogador, incluir_cartas=False, incluir_bilhetes=False)
        
        assert resultado["id"] == "1"
        assert resultado["nome"] == "Alice"
        assert resultado["cor"] == "vermelho"
        assert "trens_restantes" in resultado
        assert "cartas" not in resultado
        assert "bilhetes" not in resultado
    
    def test_formatar_jogador_com_cartas(self):
        """Testa formatação de jogador incluindo cartas"""
        jogador = Jogador(id="1", nome="Bob", cor=Cor.AZUL)
        jogador.cartasVagao = [CartaVagao(cor=Cor.VERDE, ehLocomotiva=False)]
        
        resultado = EntityFormatters.formatar_jogador(jogador, incluir_cartas=True, incluir_bilhetes=False)
        
        assert "cartas" in resultado
        assert len(resultado["cartas"]) == 1
        assert resultado["cartas"][0]["cor"] == "verde"


class TestResponseAssembler:
    """Testes para ResponseAssembler"""
    
    def test_montar_criacao_jogo_simples(self):
        """Testa montagem de resposta de criação de jogo"""
        jogador1 = Jogador(id="1", nome="Alice", cor=Cor.VERMELHO)
        
        class MockGerenciador:
            jogadores = [jogador1]
        
        class MockJogo:
            id = "game-123"
            gerenciadorDeTurnos = MockGerenciador()
            iniciado = False
            finalizado = False
        
        jogo = MockJogo()
        
        resultado = ResponseAssembler.montar_criacao_jogo(jogo, incluir_jogadores_detalhados=False)
        
        assert resultado["game_id"] == "game-123"
        assert resultado["numero_jogadores"] == 1
        assert resultado["iniciado"] is False
        assert resultado["finalizado"] is False
        assert len(resultado["jogadores"]) == 1
        assert resultado["jogadores"][0]["nome"] == "Alice"


# Fixtures para mocks
@pytest.fixture
def jogo_mock():
    """Fixture de jogo mock para testes"""
    class MockJogo:
        id = "game-test"
        iniciado = True
        finalizado = False
    
    return MockJogo()
