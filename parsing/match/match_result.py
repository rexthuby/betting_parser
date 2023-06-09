from parsing.match.MatchAttributesInterface import MatchAttributesInterface


class TeamResult:

    def __init__(self, team_name: str, score: int):
        self.team_name = team_name
        self.score = score

    @property
    def team_name(self) -> str:
        return self._team_name

    @team_name.setter
    def team_name(self, team_name: str):
        self._team_name = team_name

    @property
    def score(self) -> int:
        return self._score

    @score.setter
    def score(self, score: int):
        self._score = score

    def get_attributes_dict(self) -> dict:
        return {'team_name': self.team_name, 'score': self.score}


class MatchResult(MatchAttributesInterface):

    def __init__(self, team_results: list[TeamResult]):
        self.team_results = team_results
        self._time_score = None
    @property
    def team_results(self):
        return self._team_results

    @team_results.setter
    def team_results(self, team_results: list[TeamResult]):
        self._team_results = team_results

    @property
    def time_score(self):
        return self._time_score

    @time_score.setter
    def time_score(self, time_score: str):
        self.time_score_validate(time_score)
        self._time_score = time_score

    def time_score_validate(self, time_score):
        if '(' not in time_score or ')' not in time_score:
            raise ValueError(f'time_score is not pass validation. time_score:{time_score}')

    def get_attributes(self) -> dict:
        result = []
        for team in self.team_results:
            result.append(team.get_attributes_dict())
        return {'result': result, 'time_score': self.time_score}
