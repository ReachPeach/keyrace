import enum

from backend.game.model import Model
from backend.game.player import Player
from backend.utils import generate_id
from log import get_logger

LOG = get_logger()


class GameStateType(enum.Enum):
    IDLE = 0
    IN_PROGRESS = 1
    DONE = 2


class GameState(Model):
    def __init__(
            self,
            game_id: str,
            players: list[Player],
            text_length: int,
            id: str = generate_id(),
    ):
        self.id = id
        self.game_id = game_id
        self.players: list[Player] = players
        self.text_length = text_length

        self.type: GameStateType = GameStateType.IDLE
        self.players_score: dict[str, float] = {player.id: 0.0 for player in self.players}

    def _set_type(self, type: GameStateType):
        from storage import GameStateStorage

        LOG.debug(f"Set state for game state (game_state_id = {self.id}) to {self.type.name}")

        self.type = type

        GameStateStorage().update(self)

    def try_start(self, all_ready):
        if self.type != GameStateType.IDLE:
            LOG.debug(
                f"Failed to start game (game_id = {self.game_id}). Current game state type is {self.type.name}"
            )

            raise Exception("Game must be in IDLE to start the game")

        LOG.debug(
            f"Player (player_id = ..) is ready to start game (game_id = {self.game_id})."
        )

        if all_ready:
            LOG.debug(f"Starting game (id = {self.game_id})")
            self._set_type(GameStateType.IN_PROGRESS)

    def change_player_score(self, player_id: str, delta: float):
        from storage import GameStateStorage

        if self.type != GameStateType.IN_PROGRESS:
            LOG.debug(f"Fail to change player score (game_id = {self.game_id}, player_id = {player_id})."
                      f"Current game state type is {self.type.name}"
                      )

            raise Exception("Game state type must be IN_PROGRESS to change score")

        LOG.debug(f"Changing player score (game_id = {self.game_id}, player_id = {player_id}, delta = {delta})")

        self.players_score[player_id] += delta

        if self._check_maybe_game_end():
            LOG.debug(f"Ending game (game_id = {self.game_id})")

            self._set_type(GameStateType.DONE)

        GameStateStorage().update(self)

    def is_game_end(self) -> bool:
        return self.type == GameStateType.DONE

    def get_winner(self) -> str:
        for player in self.players:
            if self.players_score[player.id] >= self.text_length:
                return player.id

    def to_json(self):
        json = {
            "id": self.id,
            "score": self.players_score,
            "type": self.type.name,
        }

        if self.is_game_end():
            json["winner"] = self.get_winner()

        return json

    def _check_maybe_game_end(self) -> bool:
        for player in self.players:
            if self.players_score[player.id] >= self.text_length:
                return True

        return False
