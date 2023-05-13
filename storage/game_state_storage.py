from backend.game.state import GameState, GameStateType
from log import get_logger
from storage import get_driver
from storage.base_storage import BaseStorage
from .player_storage import PlayerStorage

LOG = get_logger()

DRIVER = get_driver()

player_storage = PlayerStorage()


class GameStateStorage(BaseStorage):
    INFO_TABLE_PATH = "game_states_info"
    SCORE_TABLE_PATH = "game_states_player_score"

    def insert(self, obj: GameState):
        LOG.debug(f"Creating game state (game_state_id = {obj.id})")

        DRIVER.execute_query(
            """
            insert into {table_name}
            (id, game_id, text_length, game_type)
            values
            ('{id}', '{game_id}', {text_length}, '{game_type}');
            """.format(
                table_name=self.INFO_TABLE_PATH,
                id=obj.id,
                game_id=obj.game_id,
                text_length=obj.text_length,
                game_type=obj.type.name,
            )
        )

        DRIVER.execute_query(
            """
            insert into {table_name}
            (id, player_id, score)
            values
            {values};
            """.format(
                table_name=self.SCORE_TABLE_PATH,
                values=", ".join(["('{id}', '{player_id}', {score})".format(
                    id=obj.id,
                    player_id=player.id,
                    score=obj.players_score[player.id]
                ) for player in obj.players])
            )
        )

    def update(self, obj: GameState):
        DRIVER.execute_query(
            """
            update {table_name} set
                game_id = '{game_id}',
                text_length = {text_length},
                game_type = '{game_type}'
            where
                id = '{id}';
            """.format(
                table_name=self.INFO_TABLE_PATH,
                id=obj.id,
                game_id=obj.game_id,
                text_length=obj.text_length,
                game_type=obj.type.name,
            )
        )

        for player in obj.players:
            DRIVER.execute_query(
                """
                update {table_name} set
                    score = {score}
                where
                    id = '{id}'
                    and player_id = '{player_id}';
                """.format(
                    table_name=self.SCORE_TABLE_PATH,
                    id=obj.id,
                    player_id=player.id,
                    score=obj.players_score[player.id]
                )
            )

    def select(self, **filters):
        pass

    def select_by_id(self, _id: str) -> GameState:
        info_data = DRIVER.execute_and_fetch_query("""
            select 
                game_id,
                text_length,
                game_type
            from {table_name}
            where
                id = '{id}'   
        """.format(
            table_name=self.INFO_TABLE_PATH,
            id=_id
        ))[0]

        score_data = DRIVER.execute_and_fetch_query("""
            select 
                player_id,
                score
            from {table_name}
            where
                id = '{id}'
        """.format(
            table_name=self.SCORE_TABLE_PATH,
            id=_id,
        ))

        game_state = GameState(
            id=_id,
            game_id=info_data[0],
            text_length=info_data[1],
            players=[player_storage.select_by_id(player_id) for player_id, _ in score_data]
        )
        game_state.type = GameStateType[info_data[2]]
        game_state.players_score = {
            player_id: float(score) for player_id, score in score_data
        }

        return game_state

    def delete(self, _id: str):
        pass

    def get_opened_games(self):
        ids = DRIVER.execute_and_fetch_query("""
            select 
                game_id
            from {table_name}
            where 
                game_type = 'IDLE'
        """.format(
            table_name=self.INFO_TABLE_PATH,
        ))

        return ids
