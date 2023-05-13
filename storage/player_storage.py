from backend.game.player import Player
from log import get_logger
from storage.base_storage import BaseStorage
from storage.driver import get_driver

LOG = get_logger()

DRIVER = get_driver()


class PlayerStorage(BaseStorage):
    TABLE_NAME = "players"

    def update(self, obj: Player):
        DRIVER.execute_query(
            """
            update {table_name} set
                name = '{name}',
                rating = {rating}
            where id = '{id}'
            """.format(
                table_name=self.TABLE_NAME,
                id=obj.id,
                name=obj.name,
                rating=obj.rating,
            )
        )

    def select(self, **filters) -> list[Player]:
        query = """
            select
                id,
                name,
                rating 
            from {table_name}
            where 
                {condition}
        """.format(
            table_name=self.TABLE_NAME,
            condition=" and ".join([f"{key}='{value}'" for (key, value) in filters.items()]),
        )

        data = DRIVER.execute_and_fetch_query(query)

        return [Player(
            id=_id,
            name=name,
            rating=rating
        ) for (_id, name, rating) in data]

    def select_by_id(self, _id: str) -> Player:
        return self.select(id=_id)[0]

    def insert(self, obj: Player):
        LOG.debug(f"Creating player (player_id = {obj.id})")

        DRIVER.execute_query(
            """
            insert into {table_name}
            (id, name, rating)
            values
            ('{id}', '{name}', {rating});
            """.format(
                table_name=self.TABLE_NAME,
                id=obj.id,
                name=obj.name,
                rating=obj.rating,
            )
        )

    def delete(self, _id: str):
        DRIVER.execute_query(
            """
            delete from {table_name}
            where id = '{id}'
            """.format(
                table_name=self.TABLE_NAME,
                id=_id,
            )
        )
