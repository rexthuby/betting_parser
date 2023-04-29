from parsing.match.MatchAttributesInterface import MatchAttributesInterface

class Team:
    def __init__(self, name: str, img: str):
        self.name = name
        self.img = img

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def img(self) -> str:
        return self._img

    @img.setter
    def img(self, img: str):
        self._img = img

    def get_attributes_dict(self) -> dict:
        return {'name': self.name, 'img': self.img}


class MatchTeams:
    def __init__(self, teams: list[Team]):
        self.teams = teams

    @property
    def teams(self) -> list:
        return self._teams

    @teams.setter
    def teams(self, teams: list[Team]):
        self._validate_teams(teams)
        self._teams = teams

    def get_attributes_list(self) -> list:
        result = []
        for index, team in enumerate(self.teams):
            result.append(team.get_attributes_dict())
        return result

    def _validate_teams(self, teams: list[Team]):
        if len(teams) < 2: raise Exception('List of teams are smaller than 2')


class MatchGeneralInfo(MatchAttributesInterface):

    def __init__(self, teams: MatchTeams, league: str, start: int):
        self.teams = teams
        self.league = league
        self.start = start

    @property
    def teams(self) -> MatchTeams:
        return self._teams

    @teams.setter
    def teams(self, teams: MatchTeams):
        self._teams = teams

    @property
    def league(self) -> str:
        return self._league

    @league.setter
    def league(self, league: str):
        self._league = league

    @property
    def start(self) -> int:
        """
        :return: unix time format
        """
        return self._start

    @start.setter
    def start(self, start: int):
        """
        :param start: unix time format
        """
        self._start = start

    def get_attributes(self) -> dict:
        return {'teams': self.teams.get_attributes_list(), 'league': self.league, 'start': self.start}
