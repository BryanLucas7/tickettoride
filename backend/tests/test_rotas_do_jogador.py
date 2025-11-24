"""
Testes unitários para o método Jogo.rotas_do_jogador()

Testa o helper centralizado de filtragem de rotas por jogador.
"""

import pytest
from app.core.domain.entities.jogo import Jogo
from app.core.domain.entities.jogador import Jogador
from app.core.domain.entities.cor import Cor
from app.core.domain.entities.rota import Rota
from app.core.domain.entities.cidade import Cidade
from app.core.domain.entities.tabuleiro import Tabuleiro


class TestRotasDoJogador:
    """Testes para Jogo.rotas_do_jogador()"""
    
    @pytest.fixture
    def jogo_com_rotas(self):
        """Fixture que cria um jogo com jogadores e rotas conquistadas."""
        jogo = Jogo(id=1)
        
        # Criar jogadores
        jogador1 = Jogador(id="player-1", nome="Alice", cor=Cor.AZUL)
        jogador2 = Jogador(id="player-2", nome="Bob", cor=Cor.VERMELHO)
        jogador3 = Jogador(id="player-3", nome="Carol", cor=Cor.VERDE)
        
        jogo.gerenciadorDeTurnos.adicionarJogador(jogador1)
        jogo.gerenciadorDeTurnos.adicionarJogador(jogador2)
        jogo.gerenciadorDeTurnos.adicionarJogador(jogador3)
        
        # Criar cidades
        sp = Cidade(id="SP", nome="São Paulo")
        rj = Cidade(id="RJ", nome="Rio de Janeiro")
        bsb = Cidade(id="BSB", nome="Brasília")
        ssa = Cidade(id="SSA", nome="Salvador")
        cwb = Cidade(id="CWB", nome="Curitiba")
        fln = Cidade(id="FLN", nome="Florianópolis")
        rec = Cidade(id="REC", nome="Recife")
        for_city = Cidade(id="FOR", nome="Fortaleza")
        poa = Cidade(id="POA", nome="Porto Alegre")
        mao = Cidade(id="MAO", nome="Manaus")
        bel = Cidade(id="BEL", nome="Belém")
        vix = Cidade(id="VIX", nome="Vitória")
        bh = Cidade(id="BH", nome="Belo Horizonte")
        
        # Criar rotas e atribuir proprietários
        rota1 = Rota(id="r1", cidadeA=sp, cidadeB=rj, cor=Cor.AZUL, comprimento=5)
        rota1.proprietario = jogador1
        
        rota2 = Rota(id="r2", cidadeA=bsb, cidadeB=ssa, cor=Cor.VERDE, comprimento=7)
        rota2.proprietario = jogador1
        
        rota3 = Rota(id="r3", cidadeA=cwb, cidadeB=fln, cor=Cor.VERMELHO, comprimento=3)
        rota3.proprietario = jogador2
        
        rota4 = Rota(id="r4", cidadeA=rec, cidadeB=for_city, cor=Cor.AMARELO, comprimento=4)
        rota4.proprietario = jogador2
        
        rota5 = Rota(id="r5", cidadeA=poa, cidadeB=sp, cor=Cor.PRETO, comprimento=6)
        rota5.proprietario = jogador2
        
        rota6 = Rota(id="r6", cidadeA=mao, cidadeB=bel, cor=Cor.VERDE, comprimento=8)
        rota6.proprietario = jogador3
        
        # Rota não conquistada
        rota7 = Rota(id="r7", cidadeA=vix, cidadeB=bh, cor=Cor.AZUL, comprimento=2)
        
        jogo.tabuleiro.rotas = [rota1, rota2, rota3, rota4, rota5, rota6, rota7]
        
        return jogo, jogador1, jogador2, jogador3
    
    def test_rotas_jogador_com_instancia(self, jogo_com_rotas):
        """Testa filtragem usando instância de jogador."""
        jogo, jogador1, jogador2, jogador3 = jogo_com_rotas
        
        # Jogador 1 deve ter 2 rotas
        rotas_j1 = jogo.rotas_do_jogador(jogador1)
        assert len(rotas_j1) == 2
        assert all(r.proprietario == jogador1 for r in rotas_j1)
        assert {r.id for r in rotas_j1} == {"r1", "r2"}
        
        # Jogador 2 deve ter 3 rotas
        rotas_j2 = jogo.rotas_do_jogador(jogador2)
        assert len(rotas_j2) == 3
        assert all(r.proprietario == jogador2 for r in rotas_j2)
        assert {r.id for r in rotas_j2} == {"r3", "r4", "r5"}
        
        # Jogador 3 deve ter 1 rota
        rotas_j3 = jogo.rotas_do_jogador(jogador3)
        assert len(rotas_j3) == 1
        assert rotas_j3[0].proprietario == jogador3
        assert rotas_j3[0].id == "r6"
    
    def test_rotas_jogador_com_id(self, jogo_com_rotas):
        """Testa filtragem usando ID do jogador (string)."""
        jogo, jogador1, jogador2, jogador3 = jogo_com_rotas
        
        # Buscar por ID
        rotas_j1 = jogo.rotas_do_jogador("player-1")
        assert len(rotas_j1) == 2
        assert all(r.proprietario.id == "player-1" for r in rotas_j1)
        
        rotas_j2 = jogo.rotas_do_jogador("player-2")
        assert len(rotas_j2) == 3
        assert all(r.proprietario.id == "player-2" for r in rotas_j2)
        
        rotas_j3 = jogo.rotas_do_jogador("player-3")
        assert len(rotas_j3) == 1
        assert rotas_j3[0].proprietario.id == "player-3"
    
    def test_jogador_sem_rotas(self, jogo_com_rotas):
        """Testa jogador que não conquistou nenhuma rota."""
        jogo, _, _, _ = jogo_com_rotas
        
        # Criar jogador sem rotas
        jogador4 = Jogador(id="player-4", nome="Dave", cor=Cor.AMARELO)
        jogo.gerenciadorDeTurnos.adicionarJogador(jogador4)
        
        rotas_j4 = jogo.rotas_do_jogador(jogador4)
        assert len(rotas_j4) == 0
        assert rotas_j4 == []
    
    def test_jogador_inexistente(self):
        """Testa erro ao buscar jogador inexistente por ID."""
        jogo = Jogo(id=1)
        
        with pytest.raises(ValueError, match="Jogador com ID 'inexistente' não encontrado"):
            jogo.rotas_do_jogador("inexistente")
    
    def test_rotas_nao_compartilhadas(self, jogo_com_rotas):
        """Verifica que rotas retornadas são específicas do jogador."""
        jogo, jogador1, jogador2, _ = jogo_com_rotas
        
        rotas_j1 = jogo.rotas_do_jogador(jogador1)
        rotas_j2 = jogo.rotas_do_jogador(jogador2)
        
        # Conjuntos devem ser disjuntos
        ids_j1 = {r.id for r in rotas_j1}
        ids_j2 = {r.id for r in rotas_j2}
        assert ids_j1.isdisjoint(ids_j2)
    
    def test_rotas_livres_nao_incluidas(self, jogo_com_rotas):
        """Verifica que rotas sem proprietário não são incluídas."""
        jogo, jogador1, _, _ = jogo_com_rotas
        
        rotas_j1 = jogo.rotas_do_jogador(jogador1)
        
        # Nenhuma rota livre deve aparecer
        assert all(r.proprietario is not None for r in rotas_j1)
        assert "r7" not in {r.id for r in rotas_j1}  # r7 está livre
    
    def test_retorna_lista_independente(self, jogo_com_rotas):
        """Verifica que retorna uma nova lista (não referência direta)."""
        jogo, jogador1, _, _ = jogo_com_rotas
        
        rotas1 = jogo.rotas_do_jogador(jogador1)
        rotas2 = jogo.rotas_do_jogador(jogador1)
        
        # Devem ser listas diferentes
        assert rotas1 is not rotas2
        
        # Mas com mesmo conteúdo
        assert len(rotas1) == len(rotas2)
        assert {r.id for r in rotas1} == {r.id for r in rotas2}
    
    def test_ordem_preservada(self, jogo_com_rotas):
        """Verifica que a ordem das rotas no tabuleiro é preservada."""
        jogo, _, jogador2, _ = jogo_com_rotas
        
        # Jogador 2 tem rotas r3, r4, r5 nessa ordem no tabuleiro
        rotas_j2 = jogo.rotas_do_jogador(jogador2)
        ids_ordem = [r.id for r in rotas_j2]
        
        assert ids_ordem == ["r3", "r4", "r5"]
    
    def test_performance_com_muitas_rotas(self):
        """Testa performance com grande número de rotas."""
        jogo = Jogo(id=1)
        jogador = Jogador(id="player-1", nome="Test", cor=Cor.AZUL)
        jogo.gerenciadorDeTurnos.adicionarJogador(jogador)
        
        # Criar 100 rotas, metade do jogador
        for i in range(100):
            cidade_a = Cidade(id=f"A{i}", nome=f"Cidade A{i}")
            cidade_b = Cidade(id=f"B{i}", nome=f"Cidade B{i}")
            rota = Rota(
                id=f"r{i}", 
                cidadeA=cidade_a, 
                cidadeB=cidade_b, 
                cor=Cor.AZUL, 
                comprimento=i % 10 + 1
            )
            if i % 2 == 0:
                rota.proprietario = jogador
            jogo.tabuleiro.rotas.append(rota)
        
        # Deve filtrar corretamente
        rotas_jogador = jogo.rotas_do_jogador(jogador)
        assert len(rotas_jogador) == 50
        assert all(r.proprietario == jogador for r in rotas_jogador)
