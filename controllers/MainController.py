import datetime
import json
from typing import Type

from config import SportEnum
from controllers.BaseBookmakerController import BaseBookmakerController
from misc.logger import logger
from misc.scheduler import scheduler
from models.Match import Match as MatchModel
from parsing.XbetParser import XbetParser
from parsing.match.bookmakers.XbetBookmaker import XbetBookmaker
from parsing.match.bookmakers.match_bookmaker import BookmakerNameEnum
from parsing.match.match_result import MatchResult
from typing import TypeVar

base_bookmaker_controller = TypeVar('base_bookmaker_controller', bound=BaseBookmakerController)


class MainController:

    def __init__(self, bookmaker_controllers: list[base_bookmaker_controller]):
        self._bookmaker_controllers = bookmaker_controllers

    async def parse_bookmakers(self):
        for sport in SportEnum:
            for controller in self._bookmaker_controllers:
                controller: BaseBookmakerController
                try:
                    await controller.start_parse(sport)
                except Exception as e:
                    logger.critical(f'Error in sport parsing. Sport:{sport.value}\n' + str(e), exc_info=e)
