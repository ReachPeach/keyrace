import http

import flask
from flask import session

from backend.api.v1.route import route


@route("GET", "/session/get/<key_name>")
def get(key_name: str):
    if key_name not in ['player_id', 'game_id']:
        return "'key_name' argument must be player_id or game_id", http.HTTPStatus.BAD_REQUEST

    item = session.get(key_name)
    if item is None:
        return f"No value stored for given {key_name}", http.HTTPStatus.BAD_REQUEST

    return item


@route("POST", "/session/put")
def put():
    key_name = flask.request.form.get("key_name", None)
    key_value = flask.request.form.get("key_value", None)

    if key_name not in ['player_id', 'game_id']:
        return "'key_name' argument must be player_id or game_id", http.HTTPStatus.BAD_REQUEST

    if key_value is None:
        return "'key_value' argument must be provided", http.HTTPStatus.BAD_REQUEST

    session[key_name] = key_value

    return "OK"
