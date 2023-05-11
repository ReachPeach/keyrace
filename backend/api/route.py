import functools
import http
from typing import Callable

import flask

from log import get_logger
from backend.utils import generate_id

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
                LOG.info(f"{method} call: '{blueprint.url_prefix}{url}'. Request id = {request_id}")

                ret = function(*args, **kwargs)

                LOG.info(f"Call done. Request id = {request_id}")

                return ret
            except Exception as e:
                LOG.error(f"Call fails with error '{str(e)}'. Request id = {request_id}")

                return str(e), http.HTTPStatus.INTERNAL_SERVER_ERROR

        return wrapper

    return decorator
