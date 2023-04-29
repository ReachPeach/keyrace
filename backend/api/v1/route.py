from ..route import base_rote
from .blueprint import blueprint


def route(
        method: str,
        url: str,
):
    return base_rote(
        blueprint=blueprint,
        method=method,
        url=url,
    )
