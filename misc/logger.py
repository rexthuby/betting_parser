import logging


def get_logger() -> logging:
    LOG_FILENAME = 'logs/debug.log'
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
    return logging


logger: logging.Logger = get_logger()
