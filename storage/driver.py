import os
from unittest import mock

import psycopg2

_DRIVER = None


def get_driver():
    global _DRIVER

    if _DRIVER is None:
        _DRIVER = PostgressDriver()

    return _DRIVER


class PostgressDriver:
    def __init__(self):
        if os.getenv("ENV", "COMBAT") != "TEST":
            self._connection = psycopg2.connect(dbname="db", user="admin", password="admin", host="10.5.0.3")
        else:
            self._connection = mock.MagicMock()

    def execute_query(self, query: str) -> None:
        cursor = self._connection.cursor()
        try:
            cursor.execute(query)
            cursor.close()
        except:
            cursor.close()

    def execute_and_fetch_query(self, query):
        cursor = self._connection.cursor()
        try:
            cursor.execute(query)

            data = cursor.fetchall()

            cursor.close()

            return data
        except:
            cursor.close()

            return None
