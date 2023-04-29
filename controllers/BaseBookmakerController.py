from config import SportEnum
from models.Match import match_model, Match as MatchModel
from parsing.BaseBookmakerParser import base_parser


class BaseBookmakerController:
    def __init__(self, parser: base_parser, match_model_db: match_model = MatchModel()):
        self._parser = parser
        self._match_model = match_model_db

    async def start_parse(self, sport: SportEnum):
        raise NotImplementedError

    async def parse_match_result(self, match_db_id: int):
        raise NotImplementedError
