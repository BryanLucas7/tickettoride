"""
GameService - Encapsula gerenciamento de jogos ativos e persistência.
Elimina dependência global active_games das routes.
"""
import logging
import pickle
from pathlib import Path
from typing import Dict, Optional

from ..models.entities import Jogo


class GameService:
    def __init__(self):
        self.active_games: Dict[str, Jogo] = {}
        self.games_dir = Path("games")
        self.games_dir.mkdir(exist_ok=True)

    def get_game(self, game_id: str) -> Optional[Jogo]:
        """Obtém jogo da memória ou carrega do disco."""
        if game_id in self.active_games:
            return self.active_games[game_id]
        return self._load_game(game_id)

    def save_game(self, game_id: str, jogo: Jogo) -> None:
        """Salva jogo na memória e disco."""
        self.active_games[game_id] = jogo
        self._save_game(game_id, jogo)

    def _save_game(self, game_id: str, jogo: Jogo) -> None:
        try:
            with open(self.games_dir / f"{game_id}.pkl", "wb") as f:
                pickle.dump(jogo, f)
        except Exception as e:
            logging.error(f"Erro ao salvar jogo {game_id}: {e}")

    def _load_game(self, game_id: str) -> Optional[Jogo]:
        try:
            path = self.games_dir / f"{game_id}.pkl"
            if not path.exists():
                return None
            with open(path, "rb") as f:
                jogo = pickle.load(f)
            self.active_games[game_id] = jogo
            return jogo
        except Exception as e:
            logging.error(f"Erro ao carregar jogo {game_id}: {e}")
            return None

    def list_active_games(self) -> list[str]:
        """Lista IDs de jogos ativos."""
        return list(self.active_games.keys())