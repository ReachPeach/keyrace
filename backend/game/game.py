from backend.game.model import Model
from backend.game.player import Player
from backend.game.state import GameState
from backend.utils import generate_text
from log import get_logger


LOG = get_logger()

READY: dict[str, list[int, int]] = {}

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

        if id not in READY:
            READY[id] = [0, len(players)]

    def start(self):
        READY[self.id][0] += 1

        self.game_state.try_start(READY[self.id][0] >= READY[self.id][1])

    def add_player(self, player):
        from storage import GameStorage

        READY[self.id][1] += 1

        self.players.append(player)
        self.game_state.players.append(player)

        GameStorage().add_player(self, player)

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
