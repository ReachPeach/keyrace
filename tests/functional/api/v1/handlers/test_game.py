import http
from unittest import mock

from backend.game import Game
from backend.game.player import Player
from backend.utils import generate_id, generate_text
from tests.helpers import dummy_side_effect

TEST_PLAYERS = [
    Player(
        id=generate_id(),
        name="p1",
        rating=0.0,
    ),
    Player(
        id=generate_id(),
        name="p2",
        rating=0.0,
    )
]

TEST_GAME = Game(
    id=generate_id(),
    text=generate_text(100),
    players=TEST_PLAYERS,
)


def test_create_game_ok(client):
    with (
        mock.patch(
            "storage.game_storage.GameStorage.insert",
            side_effect=dummy_side_effect
        ) as insert_game_mock,
        mock.patch(
            "storage.player_storage.PlayerStorage.select",
            return_value=TEST_PLAYERS[0],
        ) as player_select_mock
    ):
        response = client.post("/api/v1/game/create", data={
            "text_length": 100,
            "players": ",".join([player.id for player in TEST_PLAYERS])
        })

        assert response.status_code == http.HTTPStatus.OK
        player_select_mock.assert_called()
        insert_game_mock.assert_called()


def test_create_game_players_not_provided(client):
    with (
        mock.patch(
            "storage.game_storage.GameStorage.insert",
            side_effect=dummy_side_effect
        ) as insert_game_mock,
        mock.patch(
            "storage.player_storage.PlayerStorage.select",
            return_value=TEST_PLAYERS[0],
        ) as player_select_mock
    ):
        response = client.post("/api/v1/game/create", data={
            "text_length": 100,
        })

        assert response.status_code == http.HTTPStatus.BAD_REQUEST
        assert response.text == "'players' argument must be provided"
        player_select_mock.assert_not_called()
        insert_game_mock.assert_not_called()


def test_create_game_text_length_not_provided(client):
    with (
        mock.patch(
            "storage.game_storage.GameStorage.insert",
            side_effect=dummy_side_effect
        ) as insert_game_mock,
        mock.patch(
            "storage.player_storage.PlayerStorage.select",
            return_value=TEST_PLAYERS[0],
        ) as player_select_mock
    ):
        response = client.post("/api/v1/game/create", data={
            "players": ",".join([player.id for player in TEST_PLAYERS]),
        })

        assert response.status_code == http.HTTPStatus.BAD_REQUEST
        assert response.text == "'text_length' argument must be provided"
        player_select_mock.assert_not_called()
        insert_game_mock.assert_not_called()


def test_game_start_ok(client):
    with mock.patch(
            "storage.game_storage.GameStorage.select",
            return_value=TEST_GAME,
    ) as insert_game_mock:
        response = client.post("/api/v1/game/start", data={
            "id": TEST_GAME.id,
        })

        assert response.status_code == http.HTTPStatus.OK
        assert response.text == "OK"
        insert_game_mock.assert_called()


def test_game_start_id_not_provided(client):
    with mock.patch(
            "storage.game_storage.GameStorage.select",
            return_value=TEST_GAME,
    ) as insert_game_mock:
        response = client.post("/api/v1/game/start")

        assert response.status_code == http.HTTPStatus.BAD_REQUEST
        assert response.text == "'id' argument must be provided"
        insert_game_mock.assert_not_called()


def test_game_info_test_ok(client):
    with mock.patch(
            "storage.game_storage.GameStorage.select",
            return_value=TEST_GAME,
    ) as insert_game_mock:
        response = client.get(f"/api/v1/game/info?id={TEST_GAME.id}")

        assert response.status_code == http.HTTPStatus.OK
        assert response.json == TEST_GAME.to_json()
        insert_game_mock.assert_called()


def test_game_info_test_id_not_provided(client):
    with mock.patch(
            "storage.game_storage.GameStorage.select",
            return_value=TEST_GAME,
    ) as insert_game_mock:
        response = client.get(f"/api/v1/game/info")

        assert response.status_code == http.HTTPStatus.BAD_REQUEST
        assert response.text == "'id' argument must be provided"
        insert_game_mock.assert_not_called()


def test_game_state_info_test_ok(client):
    with mock.patch(
            "storage.game_storage.GameStorage.select",
            return_value=TEST_GAME,
    ) as insert_game_mock:
        response = client.get(f"/api/v1/game/state/info?id={TEST_GAME.id}")

        assert response.status_code == http.HTTPStatus.OK
        assert response.json == TEST_GAME.game_state.to_json()
        insert_game_mock.assert_called()


def test_game_state_info_test_id_not_provided(client):
    with mock.patch(
            "storage.game_storage.GameStorage.select",
            return_value=TEST_GAME,
    ) as insert_game_mock:
        response = client.get(f"/api/v1/game/state/info")

        assert response.status_code == http.HTTPStatus.BAD_REQUEST
        assert response.text == "'id' argument must be provided"
        insert_game_mock.assert_not_called()


def test_game_change_state_ok(client):
    with mock.patch(
            "storage.game_storage.GameStorage.select",
            return_value=TEST_GAME,
    ) as insert_game_mock:
        response = client.post(f"/api/v1/game/state/change", data={
            "game_id": TEST_GAME.id,
            "player_id": TEST_PLAYERS[0].id,
            "delta": 1.0,
        })

        assert response.status_code == http.HTTPStatus.OK
        assert response.text == "OK"
        insert_game_mock.assert_called()


def test_game_change_state_game_id_not_provided(client):
    with mock.patch(
            "storage.game_storage.GameStorage.select",
            return_value=TEST_GAME,
    ) as insert_game_mock:
        response = client.post(f"/api/v1/game/state/change", data={
            "player_id": TEST_PLAYERS[0].id,
            "delta": 1.0,
        })

        assert response.status_code == http.HTTPStatus.BAD_REQUEST
        assert response.text == "'game_id' argument must be provided"
        insert_game_mock.assert_not_called()


def test_game_change_state_player_id_not_provided(client):
    with mock.patch(
            "storage.game_storage.GameStorage.select",
            return_value=TEST_GAME,
    ) as insert_game_mock:
        response = client.post(f"/api/v1/game/state/change", data={
            "game_id": TEST_GAME.id,
            "delta": 1.0,
        })

        assert response.status_code == http.HTTPStatus.BAD_REQUEST
        assert response.text == "'player_id' argument must be provided"
        insert_game_mock.assert_not_called()


def test_game_change_state_delta_not_provided(client):
    with mock.patch(
            "storage.game_storage.GameStorage.select",
            return_value=TEST_GAME,
    ) as insert_game_mock:
        response = client.post(f"/api/v1/game/state/change", data={
            "game_id": TEST_GAME.id,
            "player_id": TEST_PLAYERS[0].id,
        })

        assert response.status_code == http.HTTPStatus.BAD_REQUEST
        assert response.text == "'delta' argument must be provided"
        insert_game_mock.assert_not_called()
