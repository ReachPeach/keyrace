from backend.game import Game
from backend.game.state import GameStateType
from storage.base_storage import BaseStorage


class GameStorage(BaseStorage):
    def __init__(self):
        self._games: dict[str, Game] = {}

    def insert(self, obj: object):
        pass

    def select(self, **filters):
        id = filters.get("id", None)

        if not id:
            raise Exception("'id' must be provided to load Game")

        game = self._games.get(id, None)

        if game is None:
            raise Exception(f"Game with id '{id}' not found")

        return game

    def get_opened_games(self):
        return [game_id for game_id, game in self._games.items() if game.game_state.type == GameStateType.IDLE]

    def upsert(self, obj: Game):
        self._games[obj.id] = obj

    def delete(self, id: str):
        self._games.pop(id)
