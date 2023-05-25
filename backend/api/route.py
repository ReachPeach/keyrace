import functools
import http
import traceback
from typing import Callable

import flask
import flask_sock

from backend.utils import generate_id
from log import get_logger

LOG = get_logger()


def base_rote(
        blueprint: flask.Blueprint,
        method: str,
        url: str,
):
    LOG.debug(f"Register route '{blueprint.url_prefix}{url}' with method '{method}'")

    def decorator(function: Callable):
        @functools.wraps(function)
        @blueprint.route(
            url,
            methods=[method],
        )
        def wrapper(*args, **kwargs):
            request_id = generate_id()

            try:
                LOG.info_store(
                    f"{method} call: '{blueprint.url_prefix}{url}'. Request id = {request_id}",
                    request_id=request_id
                )

                ret = function(*args, **kwargs)

                LOG.info_store(f"Call done. Request id = {request_id}", request_id=request_id)

                return ret
            except Exception as e:
                LOG.error_store(f"Call fails with error '{str(e)}'. Request id = {request_id}", request_id=request_id)
                LOG.error(traceback.format_exc())

                return str(e), http.HTTPStatus.INTERNAL_SERVER_ERROR

        return wrapper

    return decorator


def base_sock(
        sock: flask_sock.Sock,
        url: str,
):
    LOG.debug(f"Register sock '{url}'")

    def decorator(function: Callable):
        @sock.route(path=url)
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            request_id = generate_id()

            try:
                LOG.info(f"Sock call: '{url}'. Request id = {request_id}")

                ret = function(*args, **kwargs)

                LOG.info(f"Sock call done. Request id = {request_id}")

                return ret
            except Exception as e:
                LOG.error_store(
                    f"Sock call fails with error '{str(e)}'. Request id = {request_id}",
                    request_id=request_id,
                )
                LOG.error(traceback.format_exc())

                return str(e), http.HTTPStatus.INTERNAL_SERVER_ERROR

        return wrapper

    return decorator
