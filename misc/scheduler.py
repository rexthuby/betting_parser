import logging

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler


def get_jobstores():
    return {
        'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    }


def get_apscheduler_logger() -> logging.Logger:
    apscheduler_logger = logging.getLogger('apscheduler')
    apscheduler_logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler('logs/apscheduler.log')
    file_handler.setLevel(logging.WARNING)

    formatter = logging.Formatter('[%(levelname)s] - %(asctime)s - %(name)s - %(message)s')
    file_handler.setFormatter(formatter)

    apscheduler_logger.addHandler(file_handler)
    return apscheduler_logger


scheduler = AsyncIOScheduler(jobstores=get_jobstores(), logger=get_apscheduler_logger())
