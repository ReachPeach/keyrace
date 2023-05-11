import http
import random

import flask

import app
from backend.api.v1.route import route
from backend.external_api import WikipediaClient
from backend.game import Game
from backend.utils import generate_id


@route("POST", "/game/create")
def create_game():
    text_length = flask.request.form.get("text_length", None)

    if text_length is None:
        return "'text_length' argument must be provided", http.HTTPStatus.BAD_REQUEST

    text_length = int(text_length)

    players = flask.request.form.get("players", None)

    if players is None:
        return "'players' argument must be provided", http.HTTPStatus.BAD_REQUEST

    players = players.split(",")

    text = WikipediaClient().page_text("Клавогонки").replace("\n", " ")
    max_text_length = len(text)
    text_start_pos = random.randint(0, max(0, max_text_length - text_length))

    game = Game(
        id=generate_id(),
        text=text[text_start_pos: text_start_pos + text_length].strip(),
        players=[app.player_storage.select(id=player_id) for player_id in players],
    )

    app.game_storage.upsert(game)

    return game.id, http.HTTPStatus.OK


@route("POST", "/game/start")
def game_start():
    id = flask.request.form.get("id", None)

    if id is None:
        return "'id' argument must be provided", http.HTTPStatus.BAD_REQUEST

    game = app.game_storage.select(id=id)

    game.start()

    return "OK"


@route("GET", "/game/info")
def game_info():
    id = flask.request.args.get("id", None)

    if id is None:
        return "'id' argument must be provided", http.HTTPStatus.BAD_REQUEST

    game = app.game_storage.select(id=id)

    return flask.jsonify(game.to_json())


@route("GET", "/game/state/info")
def game_state_info():
    id = flask.request.args.get("id", None)

    if id is None:
        return "'id' argument must be provided", http.HTTPStatus.BAD_REQUEST

    game = app.game_storage.select(id=id)

    return flask.jsonify(game.game_state.to_json())


@route("POST", "/game/state/change")
def game_change_state():
    game_id = flask.request.form.get("game_id", None)

    if game_id is None:
        return "'game_id' argument must be provided", http.HTTPStatus.BAD_REQUEST

    player_id = flask.request.form.get("player_id", None)

    if player_id is None:
        return "'player_id' argument must be provided", http.HTTPStatus.BAD_REQUEST

    delta = flask.request.form.get("delta", None)

    if delta is None:
        return "'delta' argument must be provided", http.HTTPStatus.BAD_REQUEST

    delta = float(delta)

    game = app.game_storage.select(id=game_id)
    game.game_state.change_player_score(
        player_id=player_id,
        delta=delta,
    )

    return "OK"
