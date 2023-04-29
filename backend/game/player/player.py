from backend.game.model import Model


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

    def to_json(self):
        return {
            "id": self.id,
            "name": self._name,
            "rating": self._rating,
        }
