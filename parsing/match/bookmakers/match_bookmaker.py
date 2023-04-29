from enum import Enum
from typing import TypeVar

from parsing.match.MatchAttributesInterface import MatchAttributesInterface


class BookmakerNameEnum(Enum):
    xbet = '1xbet'


class MatchBookmaker(MatchAttributesInterface):
    def __init__(self, name: BookmakerNameEnum):
        self.name = name

    @property
    def name(self) -> BookmakerNameEnum:
        return self._name

    @name.setter
    def name(self, name: BookmakerNameEnum):
        self._name = name

    def get_attributes(self) -> dict:
        return {'name': self._name.value}


match_bookmaker = TypeVar('match_bookmaker', bound=MatchBookmaker)