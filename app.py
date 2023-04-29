import os

import flask
from flask import Flask

from backend.api.v1.blueprint import blueprint as api_v1_blueprint
from storage import PlayerStorage
from storage.game_storage import GameStorage

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

game_storage = GameStorage()
player_storage = PlayerStorage()

app = Flask(__name__)
app.register_blueprint(api_v1_blueprint)


@app.route("/", methods=["GET"])
def index():
    return flask.redirect("/api/v1/static/index.html")


if __name__ == '__main__':
    app.run()
