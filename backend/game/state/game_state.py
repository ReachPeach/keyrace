import enum

from backend.game.model import Model
from backend.game.player import Player


class GameStateType(enum.Enum):
    IDLE = 0
    IN_PROGRESS = 1
    DONE = 2


class GameState(Model):
    def __init__(
            self,
            players: list[Player],
            text_length: int,
    ):
        self._players: list[Player] = players
        self._text_length = text_length

        self._type: GameStateType = GameStateType.IDLE
        self._players_score: dict[str, float] = {player.id: 0.0 for player in self._players}

    def _set_type(self, type: GameStateType):
        self._type = type

    @property
    def player_scores(self) -> dict[str, float]:
        return self._players_score

    def try_start(self):
        if self._type != GameStateType.IDLE:
            raise Exception("Game must be in IDLE to start the game")

        self._set_type(GameStateType.IN_PROGRESS)

    def change_player_score(self, player_id: str, delta: float):
        if self._type != GameStateType.IN_PROGRESS:
            raise Exception("Game state type must be IN_PROGRESS to change score")

        self._players_score[player_id] += delta

        if self._check_maybe_game_end():
            self._set_type(GameStateType.DONE)

    def is_game_end(self) -> bool:
        return self._type == GameStateType.DONE

    def get_winner(self) -> str:
        for player in self._players:
            if self._players_score[player.id] >= self._text_length:
                return player.id

    def to_json(self):
        json = {
            "score": self.player_scores,
            "type": self._type.name,
        }

        if self.is_game_end():
            json["winner"] = self.get_winner()

        return json

    def _check_maybe_game_end(self) -> bool:
        for player in self._players:
            if self._players_score[player.id] >= self._text_length:
                return True

        return False
