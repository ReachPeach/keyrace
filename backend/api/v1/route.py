from .blueprint import blueprint
from .sock import sock
from ..route import base_rote, base_sock


def route(
        method: str,
        url: str,
):
    return base_rote(
        blueprint=blueprint,
        method=method,
        url=url,
    )


def sock_route(
        url: str,
):
    return base_sock(
        sock=sock,
        url=url,
    )
