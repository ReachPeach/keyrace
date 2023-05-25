from storage import get_driver

DRIVER = get_driver()


def init():
    DRIVER.execute_query("""
        create table if not exists players (
            id varchar(100) not null,
            name varchar(200) not null,
            rating decimal(35, 9) not null default 1000.0,
            
            constraint players_pk primary key (id)
        );
        
        create table if not exists games_info (
            id varchar(100) not null,
            name varchar(200) not null,
            text varchar(1000) not null,
            game_state_id varchar(100) not null,
            
            constraint games_info_pk primary key (id)
        );
        
        create table if not exists games_players (
            game_id varchar(100) not null,
            player_id varchar(100) not null,
            
            constraint games_players_pk primary key (game_id, player_id)
        );
        
        create type game_type_enum as enum ('IDLE', 'IN_PROGRESS', 'DONE');
        
        create table if not exists game_states_info (
            id varchar(100) not null,
            game_id varchar(100) not null,
            text_length int not null,
            game_type game_type_enum not null default 'IDLE'         
        );
        
        create table if not exists game_states_player_score (
            id varchar(100) not null,
            player_id varchar(100) not null,
            score decimal(35, 9) not null default 0.0,
            
            constraint game_states_player_score_pk primary key (id, player_id)
        );
        """
                         )

    DRIVER.execute_query(
        """
        create table if not exists logs (
            id varchar(100) not null,
            timestamp bigint not null,
            level varchar(50) not null,
            message text,
            kwargs varchar(5000),

            constraint logs_pk primary key (id)
        );
        """
    )
