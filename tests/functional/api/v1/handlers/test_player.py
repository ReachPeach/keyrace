import http
from unittest import mock

from backend.game.player import Player
from backend.utils import generate_id
from tests.helpers import dummy_side_effect

TEST_PLAYER = Player(
    id=generate_id(),
    name="abacaba",
    rating=123.01,
)


def test_create_player_ok(client):
    with mock.patch(
            "storage.player_storage.PlayerStorage.upsert",
            side_effect=dummy_side_effect
    ) as upsert_player_mock:
        response = client.post("/api/v1/player/create", data={
            "name": "abacaba"
        })

        assert response.status_code == http.HTTPStatus.OK
        upsert_player_mock.assert_called()


def test_create_player_name_not_provided(client):
    with mock.patch(
            "storage.player_storage.PlayerStorage.upsert",
            side_effect=dummy_side_effect
    ) as upsert_player_mock:
        response = client.post("/api/v1/player/create")

        assert response.status_code == http.HTTPStatus.BAD_REQUEST
        assert response.text == "'name' argument must be provided"
        upsert_player_mock.assert_not_called()


def test_player_info_ok(client):
    with mock.patch(
            "storage.player_storage.PlayerStorage.select",
            side_effect=get_player_from_storage_side_effect,
    ) as select_player_mock:
        response = client.get(f"/api/v1/player/info?id={TEST_PLAYER.id}")

        assert response.status_code == http.HTTPStatus.OK
        assert response.json == TEST_PLAYER.to_json()
        select_player_mock.assert_called()


def test_player_info_id_not_provided(client):
    with mock.patch(
            "storage.player_storage.PlayerStorage.select",
            side_effect=get_player_from_storage_side_effect,
    ) as select_player_mock:
        response = client.get(f"/api/v1/player/info")

        assert response.status_code == http.HTTPStatus.BAD_REQUEST
        assert response.text == "'id' argument must be provided"
        select_player_mock.assert_not_called()


def get_player_from_storage_side_effect(*args, **kwargs):
    return TEST_PLAYER
