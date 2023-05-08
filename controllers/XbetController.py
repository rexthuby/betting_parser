import json
import time
from datetime import datetime, timedelta

import asyncpg

from config import SportEnum
from controllers.BaseBookmakerController import BaseBookmakerController
from custom_exception.RequestError import RequestError
from custom_exception.WaitingTimeError import WaitingTimeError
from misc.logger import logger
from misc.scheduler import scheduler
from models.Match import Match as MatchModel, match_model
from parsing.XbetParser import XbetParser
from parsing.match.bookmakers.XbetBookmaker import XbetBookmaker
from parsing.match.bookmakers.match_bookmaker import BookmakerNameEnum
from parsing.match.match import Match
from parsing.match.match_result import MatchResult


class XbetController(BaseBookmakerController):
    def __init__(self, match_model_db: match_model = MatchModel(), parser: XbetParser = XbetParser()):
        super().__init__(parser, match_model_db)

    async def start_parse(self, sport: SportEnum):
        parser: XbetParser = self.parser
        try:
            matches = await parser.get_matches(sport)
        except RequestError as e:
            logger.error(e, exc_info=e)
            scheduler.add_job(self.start_parse, 'date', args=[sport],
                              run_date=datetime.now() + timedelta(minutes=30))
        else:
            for match in matches:
                try:
                    match.sport_name = sport
                    await self._parse_match(match)
                except Exception as e:
                    logger.critical(e, exc_info=e)

    async def _parse_match(self, match: Match):
        parser: XbetParser = self.parser
        bookmaker: XbetBookmaker = match.bookmaker
        try:
            match.bets = await parser.get_match_bets(bookmaker.match_id)
        except RequestError as e:
            if match.match_start_date > datetime.now().timestamp():
                logger.warning(e, exc_info=e)
                scheduler.add_job(self._parse_match, 'date', args=[match],
                                  run_date=datetime.fromtimestamp(match.match_start_date))
            else:
                logger.error(e, exc_info=e)
            return
        match_id = await self._match_model.insert_match_without_result(match)
        scheduler.add_job(self.parse_match_result, 'date', args=[match_id],
                          run_date=datetime.fromtimestamp(match.general.start) + timedelta(hours=2))

    async def parse_match_result(self, match_db_id: int):
        try:
            match_model_resp: asyncpg.Record = await self.match_model.get_all_by_id(match_db_id)
            parser: XbetParser = self.parser
            bookmaker_dict: dict = json.loads(match_model_resp['bookmaker'])
            result_url_part: str = bookmaker_dict['result_url_part']
            start_timestamp: int = match_model_resp['start_at']
            match_model: MatchModel = self.match_model
            if result_url_part is None:
                bookmaker = XbetBookmaker(BookmakerNameEnum.xbet, bookmaker_dict['match_id'])
                result_url_part = await parser.get_match_result_url_part(bookmaker.match_id)
                if result_url_part is None:
                    self._process_match_result_part_age(start_timestamp, match_db_id)
                    return
                bookmaker.match_result_url_part = result_url_part
                await match_model.update_bookmaker(match_db_id, bookmaker)
            result = await parser.get_match_result(result_url_part)
            if result is None:
                sport_enum: SportEnum = parser.parsed_data_handler.find_enum_attr(match_model_resp['sport'], SportEnum)
                if self._is_need_force_result(sport_enum, start_timestamp):
                    result = await parser.get_forced_match_result(result_url_part)
                else:
                    scheduler.add_job(self.parse_match_result, 'date', args=[match_db_id],
                                      run_date=datetime.now() + timedelta(minutes=45))
                    return
            result: MatchResult
            await match_model.update_result(match_db_id, result)
        except Exception as e:
            logger.error(e, exc_info=e)

    def _process_match_result_part_age(self, start_timestamp: int, match_db_id: int):
        if datetime.fromtimestamp(start_timestamp) + timedelta(hours=2) > datetime.now():
            raise WaitingTimeError(
                f'The duration of waiting for the result part of the match has expired. '
                f'Match start time: {datetime.fromtimestamp(start_timestamp)}. '
                f'Time of the last match result parsing: {datetime.now()}')
        scheduler.add_job(self.parse_match_result, 'date', args=[match_db_id],
                          run_date=datetime.now() + timedelta(minutes=45))

    def _is_need_force_result(self, sport: SportEnum, start: int) -> bool:
        if start + sport.max_time_duration().seconds > datetime.now().timestamp():
            return False
        return True
