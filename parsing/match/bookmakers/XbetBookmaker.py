from parsing.match.bookmakers.match_bookmaker import MatchBookmaker, BookmakerNameEnum


class XbetBookmaker(MatchBookmaker):
    def __init__(self, name: BookmakerNameEnum, match_id: int):
        super().__init__(name)
        self.match_id = match_id
        self.match_result_url_part = None

    @property
    def match_id(self) -> int:
        return self._match_id

    @match_id.setter
    def match_id(self, match_id: int):
        self._match_id = match_id

    @property
    def match_result_url_part(self) -> str:
        return self._match_result_url_part

    @match_result_url_part.setter
    def match_result_url_part(self, match_result_url_part: str):
        self._match_result_url_part = match_result_url_part

    def get_attributes(self) -> dict:
        return {'name': self.name.value, 'match_id': self.match_id,
                'result_url_part': None if self.match_result_url_part is None else self.match_result_url_part}
