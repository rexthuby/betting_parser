import json
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
        parser: XbetParser = self._parser
        try:
            matches = await parser.get_matches(sport)
        except RequestError as e:
            logger.error(e, exc_info=e)
            scheduler.add_job(self.start_parse, 'date', args=[sport],
                              run_date=datetime.now() + timedelta(minutes=30))
        else:
            for match in matches:
                try:
                    await self.__parse_match(match)
                except Exception as e:
                    logger.critical(e, exc_info=e)

    async def __parse_match(self, match: Match):
        parser: XbetParser = self._parser
        bookmaker: XbetBookmaker = match.bookmaker
        match.bets = await parser.get_match_bets(bookmaker.match_id)
        match_id = await self._match_model.insert_match_without_result(match)
        scheduler.add_job(self.parse_match_result, 'date', args=[match_id],
                          run_date=datetime.fromtimestamp(match.general.start) + timedelta(hours=1, minutes=30))

    async def parse_match_result(self, match_db_id: int):
        try:
            match_model_resp: asyncpg.Record = await self._match_model.get_all_by_id(match_db_id)
            parser: XbetParser = self._parser
            bookmaker_json = json.loads(match_model_resp['bookmaker'])
            result_url_part = bookmaker_json['result_url_part']
            start_timestamp = match_model_resp['start_at']
            if result_url_part is None:
                bookmaker = XbetBookmaker(BookmakerNameEnum.xbet, bookmaker_json['match_id'])
                result_url_part = await parser.get_match_result_url_part(bookmaker.match_id)
                if result_url_part is None:
                    self._process_match_start_age(start_timestamp, match_db_id)
                    return
                bookmaker.match_result_url_part = result_url_part
                await self._match_model.update_bookmaker(match_db_id, bookmaker)
            result = await parser.get_match_result(result_url_part)
            if result is None:
                self._process_match_start_age(start_timestamp, match_db_id)
                return
            result: MatchResult
            await self._match_model.update_result(match_db_id, result)
        except Exception as e:
            logger.error(e, exc_info=e)

    def _process_match_start_age(self, start_timestamp: int, match_db_id: int):
        if datetime.fromtimestamp(start_timestamp) + timedelta(hours=4) < datetime.now() is False:
            raise WaitingTimeError(
                f'The duration of waiting for the result of the match has expired. '
                f'Match start time: {datetime.fromtimestamp(start_timestamp)}. '
                f'Time of the last match result parsing: {datetime.now()}')
        scheduler.add_job(self.parse_match_result, 'date', args=[match_db_id],
                          run_date=datetime.now() + timedelta(minutes=15))
