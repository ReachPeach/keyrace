from backend.game.model import Model
from log import get_logger

LOG = get_logger()


class Player(Model):
    def __init__(
            self,
            id: str,
            name: str,
            rating: float,
    ):
        self.id: str = id
        self._name: str = name
        self._rating: float = rating

        LOG.debug(f"Creating player (player_id = {self.id})")

    def to_json(self):
        return {
            "id": self.id,
            "name": self._name,
            "rating": self._rating,
        }
