import logging

_LOGGER = None


def get_logger():
    global _LOGGER

    if _LOGGER is None:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%d-%m-%Y %H:%M:%S',
                            )

        _LOGGER = logging.getLogger()

    return _LOGGER
