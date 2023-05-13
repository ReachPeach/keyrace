import flask

from helpers import ROOT_DIR
from backend.api.v1.route import route


@route("GET", "/file/<path:path>")
def static(path: str):
    return flask.send_file(f"{ROOT_DIR}/files/{path}")
