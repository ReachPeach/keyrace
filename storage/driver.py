import psycopg2

_DRIVER = None


def get_driver():
    global _DRIVER

    if _DRIVER is None:
        _DRIVER = PostgressDriver()

    return _DRIVER


class PostgressDriver:
    def __init__(self):
        self._connection = psycopg2.connect(dbname="db", user="admin", password="admin", host="localhost")

    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     self._connection.close()

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
