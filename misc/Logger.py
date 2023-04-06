from loguru import logger


class Logger:
    __logger = logger

    __logger.add('logs/debug.log', format='{time:YYYY-MM-DD HH-mm-ss-SS} timezone:{time:Z} {level} file:{file} line:{line} {message}', level='INFO',
               rotation="10MB", compression='zip', backtrace=True, diagnose=True, enqueue=False, catch=True)
    @classmethod
    def get_logger(cls):
        return cls.__logger
