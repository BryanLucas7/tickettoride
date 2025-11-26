"""
Testes para PickleJogoRepository e InMemoryJogoRepository

Testa as implementações dos repository ports.
"""

import pytest
import tempfile
from pathlib import Path
from app.adapters.outbound.persistence import (
    PickleJogoRepository,
    InMemoryJogoRepository,
    PersistenceError
)
from app.core.domain.entities.jogo import Jogo
from app.core.domain.managers.gerenciador_de_turnos import GerenciadorDeTurnos


# ============================================
# FIXTURES COMPARTILHADAS (DRY)
# ============================================

@pytest.fixture
def dois_jogos():
    """
    Fixture que cria dois jogos para testes de listagem.
    
    Evita duplicação do padrão:
        jogo1 = Jogo(id=1)
        jogo2 = Jogo(id=2)
    
    que aparecia em test_listar_jogos de ambas as classes.
    """
    return [Jogo(id=1), Jogo(id=2)]


@pytest.fixture
def jogo_simples():
    """
    Fixture que cria um jogo simples para testes unitários.
    
    Centraliza a criação de jogo com id=1 usada em múltiplos testes.
    """
    return Jogo(id=1)


class TestInMemoryJogoRepository:
    """Testes para InMemoryJogoRepository."""
    
    @pytest.fixture
    def repo(self):
        """Fixture que cria um repositório in-memory limpo."""
        return InMemoryJogoRepository()
    
    def test_salvar_e_buscar_jogo(self, repo, jogo_simples):
        """Deve salvar e recuperar um jogo."""
        repo.salvar(jogo_simples)
        jogo_recuperado = repo.buscar("game-1")
        
        assert jogo_recuperado is not None
        assert jogo_recuperado.id == 1
    
    def test_buscar_jogo_inexistente(self, repo):
        """Deve retornar None para jogo inexistente."""
        jogo = repo.buscar("game-999")
        
        assert jogo is None
    
    def test_listar_jogos(self, repo, dois_jogos):
        """Deve listar todos os jogos salvos."""
        for jogo in dois_jogos:
            repo.salvar(jogo)
        jogos = repo.listar()
        
        assert len(jogos) == 2
        assert any(j.id == 1 for j in jogos)
        assert any(j.id == 2 for j in jogos)
    
    def test_listar_vazio(self, repo):
        """Deve retornar lista vazia quando não há jogos."""
        jogos = repo.listar()
        
        assert jogos == []
    
    def test_deletar_jogo_existente(self, repo, jogo_simples):
        """Deve deletar jogo existente e retornar True."""
        repo.salvar(jogo_simples)
        
        resultado = repo.deletar("game-1")
        
        assert resultado is True
        assert repo.buscar("game-1") is None
    
    def test_deletar_jogo_inexistente(self, repo):
        """Deve retornar False ao tentar deletar jogo inexistente."""
        resultado = repo.deletar("game-999")
        
        assert resultado is False
    
    def test_existe_jogo(self, repo, jogo_simples):
        """Deve verificar existência de jogo corretamente."""
        repo.salvar(jogo_simples)
        
        assert repo.existe("game-1") is True
        assert repo.existe("game-999") is False
    
    def test_limpar_todos(self, repo, dois_jogos):
        """Deve limpar todos os jogos."""
        for jogo in dois_jogos:
            repo.salvar(jogo)
        
        repo.limpar_todos()
        
        assert repo.contar() == 0
        assert repo.listar() == []


class TestPickleJogoRepository:
    """Testes para PickleJogoRepository."""
    
    @pytest.fixture
    def temp_cache_file(self):
        """Cria arquivo temporário para testes."""
        with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as f:
            cache_file = Path(f.name)
        yield cache_file
        # Cleanup
        if cache_file.exists():
            cache_file.unlink()
    
    @pytest.fixture
    def repo(self, temp_cache_file):
        """Fixture que cria um repositório Pickle com arquivo temporário."""
        return PickleJogoRepository(cache_file=temp_cache_file)
    
    def test_salvar_e_buscar_jogo(self, repo, jogo_simples):
        """Deve salvar e recuperar um jogo."""
        repo.salvar(jogo_simples)
        jogo_recuperado = repo.buscar("game-1")
        
        assert jogo_recuperado is not None
        assert jogo_recuperado.id == 1
    
    def test_persistencia_entre_instancias(self, temp_cache_file, jogo_simples):
        """Deve manter dados entre diferentes instâncias do repository."""
        # Cria repo, salva jogo e fecha
        repo1 = PickleJogoRepository(cache_file=temp_cache_file)
        repo1.salvar(jogo_simples)
        
        # Cria nova instância e verifica se jogo foi carregado
        repo2 = PickleJogoRepository(cache_file=temp_cache_file)
        jogo_recuperado = repo2.buscar("game-1")
        
        assert jogo_recuperado is not None
        assert jogo_recuperado.id == 1
    
    def test_listar_jogos(self, repo, dois_jogos):
        """Deve listar todos os jogos salvos."""
        for jogo in dois_jogos:
            repo.salvar(jogo)
        jogos = repo.listar()
        
        assert len(jogos) == 2
        assert any(j.id == 1 for j in jogos)
        assert any(j.id == 2 for j in jogos)
    
    def test_deletar_jogo(self, temp_cache_file, jogo_simples):
        """Deve deletar jogo e persistir mudança."""
        repo = PickleJogoRepository(cache_file=temp_cache_file)
        repo.salvar(jogo_simples)
        
        resultado = repo.deletar("game-1")
        
        assert resultado is True
        assert repo.buscar("game-1") is None
        
        # Verifica persistência
        repo2 = PickleJogoRepository(cache_file=temp_cache_file)
        assert repo2.buscar("game-1") is None
    
    def test_existe_jogo(self, repo, jogo_simples):
        """Deve verificar existência de jogo."""
        repo.salvar(jogo_simples)
        
        assert repo.existe("game-1") is True
        assert repo.existe("game-999") is False
    
    def test_limpar_todos(self, temp_cache_file, dois_jogos):
        """Deve limpar todos os jogos."""
        repo = PickleJogoRepository(cache_file=temp_cache_file)
        for jogo in dois_jogos:
            repo.salvar(jogo)
        
        repo.limpar_todos()
        
        assert repo.listar() == []
        
        # Verifica persistência
        repo2 = PickleJogoRepository(cache_file=temp_cache_file)
        assert repo2.listar() == []
    
    def test_cache_file_nao_existe_inicialmente(self, temp_cache_file):
        """Deve funcionar quando cache file não existe."""
        # Remove arquivo se existir
        if temp_cache_file.exists():
            temp_cache_file.unlink()
        
        repo = PickleJogoRepository(cache_file=temp_cache_file)
        
        assert repo.listar() == []
    
    def test_salvar_com_game_id_prefixado(self, repo):
        """Deve aceitar IDs já prefixados com 'game-'."""
        jogo = Jogo(id="game-abc123")
        
        repo.salvar(jogo)
        jogo_recuperado = repo.buscar("game-abc123")
        
        assert jogo_recuperado is not None
