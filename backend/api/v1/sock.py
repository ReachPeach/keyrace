from flask_sock import Sock

from .blueprint import blueprint

sock = Sock(blueprint)
