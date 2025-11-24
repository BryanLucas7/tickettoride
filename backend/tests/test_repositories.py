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


class TestInMemoryJogoRepository:
    """Testes para InMemoryJogoRepository."""
    
    def test_salvar_e_buscar_jogo(self):
        """Deve salvar e recuperar um jogo."""
        repo = InMemoryJogoRepository()
        jogo = Jogo(id=1)
        
        repo.salvar(jogo)
        jogo_recuperado = repo.buscar("game-1")
        
        assert jogo_recuperado is not None
        assert jogo_recuperado.id == 1
    
    def test_buscar_jogo_inexistente(self):
        """Deve retornar None para jogo inexistente."""
        repo = InMemoryJogoRepository()
        
        jogo = repo.buscar("game-999")
        
        assert jogo is None
    
    def test_listar_jogos(self):
        """Deve listar todos os jogos salvos."""
        repo = InMemoryJogoRepository()
        jogo1 = Jogo(id=1)
        jogo2 = Jogo(id=2)
        
        repo.salvar(jogo1)
        repo.salvar(jogo2)
        jogos = repo.listar()
        
        assert len(jogos) == 2
        assert any(j.id == 1 for j in jogos)
        assert any(j.id == 2 for j in jogos)
    
    def test_listar_vazio(self):
        """Deve retornar lista vazia quando não há jogos."""
        repo = InMemoryJogoRepository()
        
        jogos = repo.listar()
        
        assert jogos == []
    
    def test_deletar_jogo_existente(self):
        """Deve deletar jogo existente e retornar True."""
        repo = InMemoryJogoRepository()
        jogo = Jogo(id=1)
        repo.salvar(jogo)
        
        resultado = repo.deletar("game-1")
        
        assert resultado is True
        assert repo.buscar("game-1") is None
    
    def test_deletar_jogo_inexistente(self):
        """Deve retornar False ao tentar deletar jogo inexistente."""
        repo = InMemoryJogoRepository()
        
        resultado = repo.deletar("game-999")
        
        assert resultado is False
    
    def test_existe_jogo(self):
        """Deve verificar existência de jogo corretamente."""
        repo = InMemoryJogoRepository()
        jogo = Jogo(id=1)
        repo.salvar(jogo)
        
        assert repo.existe("game-1") is True
        assert repo.existe("game-999") is False
    
    def test_limpar_todos(self):
        """Deve limpar todos os jogos."""
        repo = InMemoryJogoRepository()
        repo.salvar(Jogo(id=1))
        repo.salvar(Jogo(id=2))
        
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
    
    def test_salvar_e_buscar_jogo(self, temp_cache_file):
        """Deve salvar e recuperar um jogo."""
        repo = PickleJogoRepository(cache_file=temp_cache_file)
        jogo = Jogo(id=1)
        
        repo.salvar(jogo)
        jogo_recuperado = repo.buscar("game-1")
        
        assert jogo_recuperado is not None
        assert jogo_recuperado.id == 1
    
    def test_persistencia_entre_instancias(self, temp_cache_file):
        """Deve manter dados entre diferentes instâncias do repository."""
        # Cria repo, salva jogo e fecha
        repo1 = PickleJogoRepository(cache_file=temp_cache_file)
        jogo = Jogo(id=1)
        repo1.salvar(jogo)
        
        # Cria nova instância e verifica se jogo foi carregado
        repo2 = PickleJogoRepository(cache_file=temp_cache_file)
        jogo_recuperado = repo2.buscar("game-1")
        
        assert jogo_recuperado is not None
        assert jogo_recuperado.id == 1
    
    def test_listar_jogos(self, temp_cache_file):
        """Deve listar todos os jogos salvos."""
        repo = PickleJogoRepository(cache_file=temp_cache_file)
        jogo1 = Jogo(id=1)
        jogo2 = Jogo(id=2)
        
        repo.salvar(jogo1)
        repo.salvar(jogo2)
        jogos = repo.listar()
        
        assert len(jogos) == 2
        assert any(j.id == 1 for j in jogos)
        assert any(j.id == 2 for j in jogos)
    
    def test_deletar_jogo(self, temp_cache_file):
        """Deve deletar jogo e persistir mudança."""
        repo = PickleJogoRepository(cache_file=temp_cache_file)
        jogo = Jogo(id=1)
        repo.salvar(jogo)
        
        resultado = repo.deletar("game-1")
        
        assert resultado is True
        assert repo.buscar("game-1") is None
        
        # Verifica persistência
        repo2 = PickleJogoRepository(cache_file=temp_cache_file)
        assert repo2.buscar("game-1") is None
    
    def test_existe_jogo(self, temp_cache_file):
        """Deve verificar existência de jogo."""
        repo = PickleJogoRepository(cache_file=temp_cache_file)
        jogo = Jogo(id=1)
        repo.salvar(jogo)
        
        assert repo.existe("game-1") is True
        assert repo.existe("game-999") is False
    
    def test_limpar_todos(self, temp_cache_file):
        """Deve limpar todos os jogos."""
        repo = PickleJogoRepository(cache_file=temp_cache_file)
        repo.salvar(Jogo(id=1))
        repo.salvar(Jogo(id=2))
        
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
    
    def test_salvar_com_game_id_prefixado(self, temp_cache_file):
        """Deve aceitar IDs já prefixados com 'game-'."""
        repo = PickleJogoRepository(cache_file=temp_cache_file)
        jogo = Jogo(id="game-abc123")
        
        repo.salvar(jogo)
        jogo_recuperado = repo.buscar("game-abc123")
        
        assert jogo_recuperado is not None
