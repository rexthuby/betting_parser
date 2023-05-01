import logging


def get_logger() -> logging.Logger:
    LOG_FILENAME = 'logs/main.log'
    # create logger
    logger = logging.getLogger('main_log')
    logger.setLevel(logging.DEBUG)

    # create file handler
    fh = logging.FileHandler(LOG_FILENAME)
    fh.setLevel(logging.DEBUG)

    # create formatter and add it to the file handler
    formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(message)s')
    fh.setFormatter(formatter)

    # add the file handler to the logger
    logger.addHandler(fh)

    return logger


logger: logging.Logger = get_logger()
