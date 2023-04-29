import functools
import http
from typing import Callable

import flask


def base_rote(
        blueprint: flask.Blueprint,
        method: str,
        url: str,
):
    def decorator(function: Callable):
        @functools.wraps(function)
        @blueprint.route(
            url,
            methods=[method],
        )
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception as e:
                return str(e), http.HTTPStatus.INTERNAL_SERVER_ERROR

        return wrapper

    return decorator
