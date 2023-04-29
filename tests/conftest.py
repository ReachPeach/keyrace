import pytest

from app import app as App


@pytest.fixture
def app():
    return App


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
