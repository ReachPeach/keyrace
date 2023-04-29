import flask

import app
from backend.api.v1.route import route


@route("GET", "/file/<path:path>")
def static(path: str):
    return flask.send_file(f"{app.ROOT_DIR}/files/{path}")
