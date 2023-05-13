from parsing.match.bookmakers.match_bookmaker import MatchBookmaker, BookmakerNameEnum


class XbetBookmaker(MatchBookmaker):
    def __init__(self, name: BookmakerNameEnum, match_id: int, league_id: int):
        super().__init__(name)
        self.match_id = match_id
        self.league_id = league_id
    @property
    def match_id(self) -> int:
        return self._match_id

    @match_id.setter
    def match_id(self, match_id: int):
        self._match_id = match_id

    @property
    def league_id(self) -> int:
        return self._league_id

    @league_id.setter
    def league_id(self, league_id: int):
        self._league_id = league_id

    def get_attributes(self) -> dict:
        return {'name': self.name.value, 'match_id': self._match_id, "league_id": self._league_id,}
