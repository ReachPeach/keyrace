import logging
import time

import ujson

from backend.utils import generate_id

_LOGGER = None
_STORING_LOGGER = None


class StoringLogger:
    def __init__(self, logger):
        from storage.log_storage import LogStorage

        self.logger = logger
        self.log_storage = LogStorage()

    def _store(self, message: str, level: str = "UNDEFINED", **kwargs):
        self.log_storage.insert({
            "id": generate_id(),
            "timestamp": int(time.time()),
            "level": level,
            "message": message,
            "kwargs": ujson.dumps(kwargs),
        })

    def info_store(self, message: str, **kwargs):
        self._store(message, "INFO", **kwargs)
        self.logger.info(message)

    def error_store(self, message: str, **kwargs):
        self._store(message, "ERROR", **kwargs)
        self.logger.error(message)

    def debug_store(self, message: str, **kwargs):
        self._store(message, "DEBUG", **kwargs)
        self.logger.debug(message)

    def warning_store(self, message: str, **kwargs):
        self._store(message, "WARNING", **kwargs)
        self.logger.warning(message)

    def info(self, message: str):
        self.logger.info(message)

    def error(self, message: str):
        self.logger.error(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def warning(self, message: str):
        self.logger.warning(message)


def get_logger():
    global _LOGGER
    global _STORING_LOGGER

    if _LOGGER is None:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%d-%m-%Y %H:%M:%S',
                            )

        _LOGGER = logging.getLogger()

    if _STORING_LOGGER is None:
        _STORING_LOGGER = StoringLogger(_LOGGER)

    return _STORING_LOGGER
