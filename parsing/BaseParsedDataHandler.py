import enum
from datetime import datetime, timedelta
import math
from typing import TypeVar, Any

from custom_exception.ParsingError import ParsingError
from misc.datetime_run_managment.ScriptRun import ScriptRun
from parsing.match.bookmakers.match_bookmaker import BookmakerNameEnum


class BaseParsedDataHandler:
    def __init__(self, bookmaker_name: BookmakerNameEnum):
        self._bookmaker_name = bookmaker_name

    @staticmethod
    def _is_valid_start_date(start_date: int) -> bool:
        """
        :param start_date: timestamp date
        """
        script_run: ScriptRun = ScriptRun()
        last_run_date = script_run.get_last_run()
        if last_run_date is None:
            raise ParsingError('Dont have last run date')
        daily_script_start_at = math.trunc(datetime.timestamp(script_run.get_last_run()))
        script_interval_run = timedelta(seconds=script_run.SECONDS_PER_RUN).total_seconds()

        if daily_script_start_at + script_interval_run < start_date:
            return False
        return True

    @staticmethod
    def find_enum_attr(desired_value, enum_class: enum.EnumType) -> Any | None:
        for member in enum_class.__members__.values():
            if member.value == desired_value:
                return member
        return None


base_parsed_data_handler = TypeVar('base_parsed_data_handler', bound=BaseParsedDataHandler)
