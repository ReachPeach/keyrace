import abc


class Model(abc.ABC):

    @abc.abstractmethod
    def to_json(self):
        pass
