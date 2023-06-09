from backend.game import Game
from log import get_logger
from storage import get_driver
from storage.base_storage import BaseStorage
from .game_state_storage import GameStateStorage
from .player_storage import PlayerStorage

LOG = get_logger()

DRIVER = get_driver()

player_storage = PlayerStorage()
game_state_storage = GameStateStorage()


class GameStorage(BaseStorage):
    INFO_TABLE_PATH = "games_info"
    PLAYERS_TABLE_PATH = "games_players"

    def select(self, **filters):
        pass

    def select_by_id(self, _id: str) -> Game:
        info_data = DRIVER.execute_and_fetch_query("""
                    select 
                        name,
                        text,
                        game_state_id
                    from {table_name}
                    where
                        id = '{id}'
                """.format(
            table_name=self.INFO_TABLE_PATH,
            id=_id
        ))[0]

        players_data = DRIVER.execute_and_fetch_query("""
                    select 
                        player_id
                    from {table_name}
                    where
                        game_id = '{id}'
                """.format(
            table_name=self.PLAYERS_TABLE_PATH,
            id=_id,
        ))

        game = Game(
            id=_id,
            name=info_data[0],
            text=info_data[1],
            players=[player_storage.select_by_id(player_data[0]) for player_data in players_data]
        )
        game.game_state = game_state_storage.select_by_id(info_data[2])

        return game

    def insert(self, obj: Game):
        LOG.debug(f"Creating game (game_id = {obj.id})")

        DRIVER.execute_query("""
            insert into {table_name}
            (id, name, text, game_state_id)
            values
            ('{id}', '{name}', '{text}', '{game_state_id}')
        """.format(
            table_name=self.INFO_TABLE_PATH,
            id=obj.id,
            name=obj.name,
            text=obj.text,
            game_state_id=obj.game_state.id,
        ))

        game_state_storage.insert(obj.game_state)

        DRIVER.execute_query("""
            insert into {table_name}
            (game_id, player_id)
            values
            {values}
        """.format(
            table_name=self.PLAYERS_TABLE_PATH,
            values=", ".join(["('{game_id}', '{player_id}')".format(
                game_id=obj.id,
                player_id=player.id
            ) for player in obj.players])
        ))

    def update(self, obj: object):
        pass

    def delete(self, id: str):
        pass

    def add_player(self, obj: Game, player):
        DRIVER.execute_query("""
            insert into {table_name}
            (game_id, player_id)
            values
            ('{game_id}', '{player_id}')
        """.format(
            table_name=self.PLAYERS_TABLE_PATH,
            game_id=obj.id,
            player_id=player.id,
        ))

        DRIVER.execute_query("""
            insert into {table_name}
            (id, player_id)
            values
            ('{game_state_id}', '{player_id}')
        """.format(
            table_name=GameStateStorage.SCORE_TABLE_PATH,
            game_state_id=obj.game_state.id,
            player_id=player.id,
        ))
