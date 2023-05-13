import os

import flask
from flask import Flask

from backend.api.v1.blueprint import blueprint as api_v1_blueprint
from storage import get_driver
from storage.pre_init import init as create_tables_init

create_tables_init()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.register_blueprint(api_v1_blueprint)

@app.route("/", methods=["GET"])
def index():
    return flask.redirect("/api/v1/file/index.html")


if __name__ == '__main__':
    app.run()
