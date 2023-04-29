import http

import flask

import app
from backend.api.v1.route import route
from backend.game.player import Player
from backend.utils import generate_id


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

    app.player_storage.upsert(player)

    return player.id, http.HTTPStatus.OK


@route("GET", "/player/info")
def player_info():
    id = flask.request.args.get("id", None)

    if id is None:
        return "'id' argument must be provided", http.HTTPStatus.BAD_REQUEST

    player = app.player_storage.select(id=id)

    return flask.jsonify(player.to_json())
