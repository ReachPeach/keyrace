import http

import flask

from backend.api.v1.route import route
from backend.game.player import Player
from backend.utils import generate_id
from storage import PlayerStorage

player_storage = PlayerStorage()


@route("POST", "/player/create")
def create_player():
    name = flask.request.form.get("name", None)

    if name is None:
        return "'name' argument must be provided", http.HTTPStatus.BAD_REQUEST

    player = Player(
        id=generate_id(),
        name=name,
        rating=0.0,
    )

    player_storage.insert(player)

    return player.id, http.HTTPStatus.OK


@route("GET", "/player/info")
def player_info():
    id = flask.request.args.get("id", None)

    if id is None:
        return "'id' argument must be provided", http.HTTPStatus.BAD_REQUEST

    player = player_storage.select_by_id(id)

    return flask.jsonify(player.to_json())
