from storage import get_driver
from storage.base_storage import BaseStorage

DRIVER = get_driver()


class LogStorage(BaseStorage):
    TABLE_NAME = "logs"

    def insert(self, obj: dict):
        DRIVER.execute_query("""
                        insert into {table_name}
                        (id, timestamp, level, message, kwargs)
                        values
                        ('{id}', {timestamp}, '{level}', '{message}', '{kwargs}') 
                    """.format(
            table_name=self.TABLE_NAME,
            id=obj["id"],
            timestamp=obj["timestamp"],
            level=obj["level"],
            # message=obj["message"].replace('\'', '\\\''),
            message="abacaba",
            # kwargs=obj["kwargs"],
            kwargs="",
        ))

    def update(self, obj: object):
        pass

    def select(self, **filters):
        pass

    def delete(self, id: str):
        pass
