from backend.game.model import Model
from backend.utils import generate_id, generate_text
from log import get_logger

LOG = get_logger()


class Player(Model):
    def __init__(
            self,
            rating: float,
            name: str = generate_text(50),
            id: str = generate_id(),
    ):
        self.id: str = id
        self.name: str = name
        self.rating: float = rating

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "rating": self.rating,
        }
