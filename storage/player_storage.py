from backend.game.player import Player
from storage.base_storage import BaseStorage


class PlayerStorage(BaseStorage):
    def __init__(self):
        self._players: dict[str, Player] = {}

    def insert(self, obj: object):
        pass

    def select(self, **filters) -> Player:
        id = filters.get("id", None)

        if not id:
            raise Exception("'id' must be provided to load Game")

        player = self._players.get(id, None)

        if player is None:
            raise Exception(f"Player with id '{id}' not fount")

        return player

    def upsert(self, obj: Player):
        self._players[obj.id] = obj

    def delete(self, id: str):
        self._players.pop(id)
