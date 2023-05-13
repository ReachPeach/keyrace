from typing import Optional

from backend.game.model import Model
from backend.game.player import Player
from backend.game.state import GameState
from backend.utils import generate_text
from log import get_logger

LOG = get_logger()


class Game(Model):
    def __init__(
            self,
            id: str,
            text: str,
            players: list[Player],
            name: str = generate_text(50),
    ):
        self.id: str = id
        self.name: str = name
        self.text: str = text
        self.players: list[Player] = players

        self.game_state: GameState = GameState(
            game_id=self.id,
            players=self.players,
            text_length=len(text),
        )

        LOG.debug(f"Creating game (game_id = {self.id})")

    def start(self, player):
        self.game_state.try_start(player)

    def add_player(self, player):
        self._players.add(player)
        self.game_state.add_player(player)

    def is_game_end(self) -> bool:
        return self.game_state.is_game_end()

    def get_winner(self) -> str:
        return self.game_state.get_winner()

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "text": self.text,
            "players": ",".join([player.id for player in self.players]),
        }
