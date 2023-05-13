import json
from datetime import datetime, timedelta

import asyncpg

from config import SportEnum
from controllers.BaseBookmakerController import BaseBookmakerController
from custom_exception.RequestError import RequestError
from misc.datetime_run_managment.ScriptRun import ScriptRun
from misc.datetime_run_managment.ScriptRunInterface import ScriptRunInterface
from misc.logger import logger
from misc.scheduler import scheduler
from models.Match import Match as MatchModel, match_model
from parsing.XbetParser import XbetParser
from parsing.match.bookmakers.XbetBookmaker import XbetBookmaker
from parsing.match.bookmakers.match_bookmaker import BookmakerNameEnum
from parsing.match.match import Match
from parsing.match.match_general_info import MatchGeneralInfo, MatchTeams, Team
from parsing.match.match_result import MatchResult


class XbetController(BaseBookmakerController):
    def __init__(self, match_model_db: match_model = MatchModel(), parser: XbetParser = XbetParser()):
        super().__init__(parser, match_model_db)

    async def start_parse(self, sport: SportEnum):
        parser: XbetParser = self.parser
        try:
            matches = await parser.get_matches(sport)
        except RequestError as e:
            script_run_manager: ScriptRunInterface = ScriptRun()
            if script_run_manager.get_last_run() + timedelta(hours=1) < datetime.now():
                logger.critical(e, exc_info=e)
            else:
                logger.error(e, exc_info=e)
                scheduler.add_job(self.start_parse, 'date', args=[sport],
                                  run_date=datetime.now() + timedelta(minutes=5), misfire_grace_time=60 * 60)
        else:
            for match in matches:
                try:
                    match.sport_name = sport
                    await self._parse_match(match, sport)
                except Exception as e:
                    logger.critical(e, exc_info=e)

    async def _parse_match(self, match: Match, sport: SportEnum):
        parser: XbetParser = self.parser
        bookmaker: XbetBookmaker = match.bookmaker
        try:
            match.bets = await parser.get_match_bets(bookmaker.match_id)
        except RequestError as e:
            if match.match_start_date > datetime.now().timestamp():
                logger.warning(e, exc_info=e)
                scheduler.add_job(self._parse_match, 'date', args=[match], misfire_grace_time=60 * 60,
                                  run_date=datetime.fromtimestamp(match.match_start_date))
            else:
                logger.error(e, exc_info=e)
            return
        match_id = await self._match_model.insert_match_without_result(match)
        scheduler.add_job(self.parse_match_result, 'date', args=[match_id], misfire_grace_time=60 * 60,
                          run_date=datetime.fromtimestamp(match.match_start_date) + sport.medium_game_duration())

    async def parse_match_result(self, match_db_id: int):
        try:
            match_model_resp: asyncpg.Record = await self.match_model.get_all_by_id(match_db_id)
            parser: XbetParser = self.parser
            bookmaker_dict: dict = json.loads(match_model_resp['bookmaker'])
            start_timestamp: int = match_model_resp['start_at']
            bookmaker = XbetBookmaker(BookmakerNameEnum.xbet, bookmaker_dict['match_id'], bookmaker_dict['league_id'])
            general_json = json.loads(match_model_resp['general'])
            teams: list = general_json['teams']
            match_teams = MatchTeams([Team(teams[0]['name'], teams[0]['img']),
                                      Team(teams[1]['name'], teams[1]['img'])])
            general = MatchGeneralInfo(match_teams, general_json['league'], start_timestamp)
            result = await parser.get_match_result(match_model_resp['name'], general, bookmaker)

            if isinstance(result, MatchResult):
                match_model: MatchModel = self.match_model
                await match_model.update_result(match_db_id, result)
                return

            sport_enum: SportEnum = parser.parsed_data_handler.find_enum_attr(match_model_resp['sport'], SportEnum)
            if self._is_exceeded_maximum_wait(sport_enum, start_timestamp):
                logger.debug(
                    f'The maximum expectation of the result of the match has been exceeded. Match id:{match_db_id}')
                return

            scheduler.add_job(self.parse_match_result, 'date', args=[match_db_id], misfire_grace_time=60 * 60,
                              run_date=datetime.now() + timedelta(minutes=20))

        except Exception as e:
            logger.error(e, exc_info=e)

    def _is_exceeded_maximum_wait(self, sport: SportEnum, start: int) -> bool:
        if start + sport.max_game_duration().total_seconds() > datetime.now().timestamp():
            return False
        return True
