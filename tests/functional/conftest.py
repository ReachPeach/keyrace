import threading

import pytest
from selenium import webdriver

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


@pytest.fixture()
def driver(app):
    driver = webdriver.Chrome()
    driver.get('http://127.0.0.1:5000/api/v1/file/index.html')
    yield driver
    driver.quit()
