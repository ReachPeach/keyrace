import threading

import pytest

from app import index
from app import app as App
from selenium import webdriver


@pytest.fixture
def app():
    tread = threading.Thread(target=App.run)
    tread.start()
    return App


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def driver(app):
    driver = webdriver.Chrome()
    driver.get('http://127.0.0.1:5000/api/v1/file/index.html')
    yield driver
    driver.quit()
