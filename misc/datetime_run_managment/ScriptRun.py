from datetime import datetime, timedelta

from misc.datetime_run_managment.FileKeyError import FileKeyError
from misc.datetime_run_managment.ScriptRunInterface import ScriptRunInterface
from misc.datetime_run_managment.FileManager import FileManager
from misc.datetime_run_managment.KeyValueManagerInterface import KeyValueManagerInterface
from misc.logger import logger


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class ScriptRun(ScriptRunInterface):
    SECONDS_PER_RUN = 43200  # 12 hours in seconds
    LAST_RUN_KEY = 'last_run_datetime'
    LAST_RUN_VALUE_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, key_value_manager: KeyValueManagerInterface = FileManager('script_run_datetime_info.txt')):
        self._key_value_manager = key_value_manager

    def get_last_run(self) -> datetime | None:
        file_manager = self._key_value_manager
        try:
            last_run_date = file_manager.get_value(self.LAST_RUN_KEY)
        except FileKeyError as e:
            logger.info(e, exc_info=e)
            return None
        except Exception as e:
            logger.warning(e, exc_info=e)
            return None
        if last_run_date is None:
            return None
        return datetime.strptime(last_run_date, self.LAST_RUN_VALUE_FORMAT)

    def get_next_run(self) -> datetime | None:
        """
        :return: gives next run date based on last run date
        """
        last_run_datetime = self.get_last_run()
        if last_run_datetime is None:
            return None
        return last_run_datetime + timedelta(seconds=self.SECONDS_PER_RUN)

    def set_last_run(self, date: datetime) -> datetime:
        """
        :return: saved datetime run
        """
        last_run_datetime = datetime(date.year, date.month, date.day, date.hour, date.minute)
        self._key_value_manager.save_or_update_key(self.LAST_RUN_KEY,
                                                   last_run_datetime.strftime(self.LAST_RUN_VALUE_FORMAT))
        return last_run_datetime
