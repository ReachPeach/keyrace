from typing import Optional

from backend.game.model import Model
from backend.game.player import Player
from backend.game.state import GameState
from log import get_logger

LOG = get_logger()


class Game(Model):
    def __init__(
            self,
            id: str,
            text: str,
            players: list[Player],
            name: Optional[str] = None,
    ):
        self.id: str = id
        self._name: Optional[str] = name
        self._text: str = text
        self._players: list[Player] = players

        self.game_state: GameState = GameState(
            game_id=self.id,
            players=self.players,
            text_length=len(text),
        )

        LOG.debug(f"Creating game (game_id = {self.id})")

    @property
    def players(self) -> list[Player]:
        return self._players

    def start(self):
        self.game_state.try_start()

    def is_game_end(self) -> bool:
        return self.game_state.is_game_end()

    def get_winner(self) -> str:
        return self.game_state.get_winner()

    def to_json(self):
        return {
            "id": self.id,
            "name": self._name,
            "text": self._text,
            "players": ",".join([player.id for player in self._players]),
        }
