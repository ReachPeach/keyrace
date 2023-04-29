import abc


class BaseStorage(abc.ABC):
    @abc.abstractmethod
    def insert(self, obj: object):
        pass

    @abc.abstractmethod
    def upsert(self, obj: object):
        pass

    @abc.abstractmethod
    def select(self, **filters):
        pass

    @abc.abstractmethod
    def delete(self, id: str):
        pass
