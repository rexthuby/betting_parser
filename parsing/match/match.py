from abc import ABC, abstractmethod

from parsing.match.bets.bet import MatchBets
from parsing.match.bookmakers.XbetBookmaker import XbetBookmaker
from parsing.match.bookmakers.match_bookmaker import MatchBookmaker, match_bookmaker
from parsing.match.match_general_info import MatchGeneralInfo
from parsing.match.match_result import MatchResult


class Match:
    def __init__(self, name: str, bookmaker: MatchBookmaker, match_start_date: int):
        self.name = name
        self.bookmaker = bookmaker
        self.match_start_date = match_start_date
        self._general = None
        self._bets = None
        self._result = None

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def bookmaker(self) -> match_bookmaker:
        return self._bookmaker

    @bookmaker.setter
    def bookmaker(self, bookmaker: MatchBookmaker):
        self._bookmaker = bookmaker

    @property
    def general(self) -> MatchGeneralInfo | None:
        return self._general

    @general.setter
    def general(self, general: MatchGeneralInfo):
        self._general = general

    @property
    def bets(self) -> MatchBets | None:
        return self._bets

    @bets.setter
    def bets(self, bets: MatchBets):
        self._bets = bets

    @property
    def result(self) -> MatchResult | None:
        return self._result

    @result.setter
    def result(self, result: MatchResult):
        self._result = result

    @property
    def match_start_date(self) -> int:
        """
        :return: start datetime in unix format
        """
        return self._match_start_date

    @match_start_date.setter
    def match_start_date(self, match_start_date: int):
        """
        :param match_start_date: unix-time format
        """
        self._match_start_date = match_start_date

    def get_attributes_dict(self):
        return {
            'name': self._name,
            'match_start_date': self._match_start_date,
            'bookmaker': self._bookmaker.get_attributes(),
            'general': None if self._general is None else self._general.get_attributes(),
            'bets': None if self._bets is None else self._bets.get_attributes(),
            'result': None if self._result is None else self._result.get_attributes()
        }
