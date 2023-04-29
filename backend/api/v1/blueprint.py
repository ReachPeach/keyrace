import flask

blueprint = flask.Blueprint(
    name="api",
    import_name=__name__,
    url_prefix="/api/v1",
)
