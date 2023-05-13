import copy
import http
import random
from time import sleep

import flask
import ujson

import app
from backend.api.v1.route import route, sock_route
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
        players = set()
    else:
        players = players.split(",")

    text = WikipediaClient().page_text("Клавогонки").replace("\n", " ")
    max_text_length = len(text)
    text_start_pos = random.randint(0, max(0, max_text_length - text_length))

    game = Game(
        id=generate_id(),
        text=text[text_start_pos: text_start_pos + text_length].strip(),
        players=set([app.player_storage.select(id=player_id) for player_id in players]),
    )
    print(game.players)

    app.game_storage.upsert(game)

    return game.id, http.HTTPStatus.OK


@route("POST", "/game/start")
def game_start():
    game_id = flask.request.form.get("game_id", None)

    if game_id is None:
        return "'game_id' argument must be provided", http.HTTPStatus.BAD_REQUEST

    player_id = flask.request.form.get("player_id", None)

    if player_id is None:
        return "'player_id' argument must be provided", http.HTTPStatus.BAD_REQUEST

    game = app.game_storage.select(id=game_id)
    player = app.player_storage.select(id=player_id)
    game.start(player)

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


@sock_route("/m/game/state")
def monitor_game_state(sock):
    id = flask.request.args.get("game_id", None)

    if id is None:
        return "'id' argument must be provided", http.HTTPStatus.BAD_REQUEST
    game = app.game_storage.select(id=id)
    prev_state = copy.copy(game.game_state.type)
    while True:
        if game.game_state.type != prev_state:
            prev_state = copy.copy(game.game_state.type)
            sock.send(ujson.dumps(game.game_state.to_json()))


@sock_route("/m/game")
def monitor_game(sock):
    id = flask.request.args.get("game_id", None)

    if id is None:
        return "'id' argument must be provided", http.HTTPStatus.BAD_REQUEST
    save_count = len(app.game_storage.select(id=id).players)

    while True:
        game = app.game_storage.select(id=id)
        current_count = len(game.players)
        if save_count != current_count:
            save_count = current_count
            sock.send(ujson.dumps(game.to_json()))
        else:
            sleep(1)


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


@route("GET", '/games/ids')
def opened_games():
    game_ids = app.game_storage.get_opened_games()
    return flask.jsonify({"ids": game_ids})


@route("POST", '/game/join')
def join_game():
    game_id = flask.request.form.get("game_id", None)

    if game_id is None:
        return "'game_id' argument must be provided", http.HTTPStatus.BAD_REQUEST

    player_id = flask.request.form.get("player_id", None)

    if player_id is None:
        return "'player_id' argument must be provided", http.HTTPStatus.BAD_REQUEST

    game = app.game_storage.select(id=game_id)
    player = app.player_storage.select(id=player_id)
    game.add_player(player)

    return "OK"
