from typing import TypeVar

from config import SportEnum
from models.Match import match_model, Match as MatchModel
from parsing.BaseBookmakerParser import base_parser


class BaseBookmakerController:
    def __init__(self, parser: base_parser, match_model_db: match_model = MatchModel()):
        self.parser = parser
        self.match_model = match_model_db

    @property
    def parser(self) -> base_parser:
        return self._parser

    @parser.setter
    def parser(self, parser: base_parser):
        self._parser = parser

    @property
    def match_model(self) -> match_model:
        return self._match_model

    @match_model.setter
    def match_model(self, match_model_db: match_model):
        self._match_model = match_model_db

    async def start_parse(self, sport: SportEnum):
        raise NotImplementedError

    async def parse_match_result(self, match_db_id: int):
        raise NotImplementedError


base_bookmaker_controller = TypeVar('base_bookmaker_controller', bound=BaseBookmakerController)
