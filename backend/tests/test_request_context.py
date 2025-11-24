"""
Testes para request_context.py

Verifica que GameRequestContext e PlayerRequestContext funcionam corretamente
e reduzem boilerplate nos endpoints.
"""
import sys
from pathlib import Path

# Adicionar o diretório backend ao path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

import pytest
from fastapi import HTTPException
from unittest.mock import Mock

from app.shared.request_context import (
    GameRequestContext,
    PlayerRequestContext,
    get_game_context,
    get_player_context
)
from app.core.domain.entities.jogo import Jogo
from app.core.domain.entities.jogador import Jogador
from app.application.services.game_service import GameService


class TestGameRequestContext:
    """Testa GameRequestContext"""
    
    def test_game_context_structure(self):
        """Verifica que GameRequestContext tem os atributos corretos"""
        mock_jogo = Mock(spec=Jogo)
        mock_service = Mock(spec=GameService)
        
        ctx = GameRequestContext(
            game_id="test-123",
            jogo=mock_jogo,
            game_service=mock_service
        )
        
        assert ctx.game_id == "test-123"
        assert ctx.jogo is mock_jogo
        assert ctx.game_service is mock_service
    
    def test_get_game_context_factory(self):
        """Verifica que get_game_context cria contexto corretamente"""
        mock_jogo = Mock(spec=Jogo)
        mock_service = Mock(spec=GameService)
        
        ctx = get_game_context(
            game_id="test-123",
            jogo=mock_jogo,
            game_service=mock_service
        )
        
        assert isinstance(ctx, GameRequestContext)
        assert ctx.game_id == "test-123"
        assert ctx.jogo is mock_jogo
        assert ctx.game_service is mock_service


class TestPlayerRequestContext:
    """Testa PlayerRequestContext"""
    
    def test_player_context_structure(self):
        """Verifica que PlayerRequestContext tem os atributos corretos"""
        mock_jogo = Mock(spec=Jogo)
        mock_jogador = Mock(spec=Jogador)
        mock_service = Mock(spec=GameService)
        
        ctx = PlayerRequestContext(
            game_id="test-123",
            jogo=mock_jogo,
            game_service=mock_service,
            player_id="player-456",
            jogador=mock_jogador
        )
        
        assert ctx.game_id == "test-123"
        assert ctx.jogo is mock_jogo
        assert ctx.game_service is mock_service
        assert ctx.player_id == "player-456"
        assert ctx.jogador is mock_jogador
    
    def test_player_context_inherits_from_game_context(self):
        """Verifica que PlayerRequestContext herda de GameRequestContext"""
        assert issubclass(PlayerRequestContext, GameRequestContext)
    
    def test_get_player_context_factory(self):
        """Verifica que get_player_context cria contexto corretamente"""
        mock_jogo = Mock(spec=Jogo)
        mock_jogador = Mock(spec=Jogador)
        mock_service = Mock(spec=GameService)
        
        ctx = get_player_context(
            game_id="test-123",
            player_id="player-456",
            jogo=mock_jogo,
            jogador=mock_jogador,
            game_service=mock_service
        )
        
        assert isinstance(ctx, PlayerRequestContext)
        assert ctx.game_id == "test-123"
        assert ctx.player_id == "player-456"
        assert ctx.jogo is mock_jogo
        assert ctx.jogador is mock_jogador
        assert ctx.game_service is mock_service


class TestContextIntegration:
    """Testa integração dos contextos com endpoints"""
    
    def test_context_reduces_parameters(self):
        """
        Demonstra redução de boilerplate:
        
        ANTES (5 parâmetros):
        def endpoint(game_id, player_id, jogo, jogador, game_service):
            ...
        
        DEPOIS (1 parâmetro):
        def endpoint(ctx: PlayerRequestContext = Depends(get_player_context)):
            ...
        """
        # Setup
        mock_jogo = Mock(spec=Jogo)
        mock_jogador = Mock(spec=Jogador)
        mock_service = Mock(spec=GameService)
        
        # Simula endpoint antigo (múltiplos parâmetros)
        def old_endpoint(game_id, player_id, jogo, jogador, game_service):
            return {
                "game_id": game_id,
                "player_id": player_id,
                "jogo": jogo,
                "jogador": jogador,
                "service": game_service
            }
        
        # Simula endpoint novo (contexto único)
        def new_endpoint(ctx: PlayerRequestContext):
            return {
                "game_id": ctx.game_id,
                "player_id": ctx.player_id,
                "jogo": ctx.jogo,
                "jogador": ctx.jogador,
                "service": ctx.game_service
            }
        
        # Cria contexto
        ctx = get_player_context(
            game_id="test-123",
            player_id="player-456",
            jogo=mock_jogo,
            jogador=mock_jogador,
            game_service=mock_service
        )
        
        # Chama ambos endpoints
        old_result = old_endpoint("test-123", "player-456", mock_jogo, mock_jogador, mock_service)
        new_result = new_endpoint(ctx)
        
        # Verifica que ambos produzem o mesmo resultado
        assert old_result == new_result
