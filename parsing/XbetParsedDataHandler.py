from typing import Any

from bs4 import BeautifulSoup, Tag

from custom_exception.ParsingError import ParsingError
from misc.logger import logger
from parsing.BaseParsedDataHandler import BaseParsedDataHandler
from parsing.match.bets.bet import MatchBets, BetNameEnum, Bet
from parsing.match.bets.coefficient import Coefficient, Total
from parsing.match.bookmakers.XbetBookmaker import XbetBookmaker
from parsing.match.bookmakers.match_bookmaker import BookmakerNameEnum
from parsing.match.match import Match
from parsing.match.match_general_info import MatchGeneralInfo, MatchTeams, Team
from parsing.match.match_result import MatchResult, TeamResult


class XbetParsedDataHandler(BaseParsedDataHandler):
    _bet_name_enum_to_id = {BetNameEnum.one_x_two: 1, BetNameEnum.team_wins: 101,
                            BetNameEnum.double_chance: 8, BetNameEnum.total: 17,
                            BetNameEnum.both_goal: 19}

    _forbidden_words = ("хозяев", "команды")

    def __init__(self):
        super().__init__(BookmakerNameEnum.xbet)

    def get_matches(self, r) -> list[Match]:
        matches = []
        for match_r in r['Value']:
            try:
                if len(match_r['AE']) == 0:
                    continue
                match_start_timestamp_date = int(match_r['S'])
                if self._is_valid_start_date(match_start_timestamp_date) is False:
                    continue
                if self.check_substrings_in_string(match_r["O1"].lower(), self._forbidden_words) or \
                        self.check_substrings_in_string(match_r["O2"].lower(), self._forbidden_words):
                    continue
                match = self._prepare_match(match_r)
                matches.append(match)
            except Exception as e:
                logger.error('Incorrect processing of data from 1xbet', exc_info=e)
        if len(matches) < 1:
            raise ParsingError('Matches array is empty')
        return matches

    def _prepare_match(self, match_r) -> Match:
        team_1_name = match_r["O1"]
        team_1_img = f'https://v2l.traincdn.com/sfiles/logo_teams/{match_r["O1IMG"][0]}.png'
        team_2_name = match_r["O2"]
        team_2_img = f'https://v2l.traincdn.com/sfiles/logo_teams/{match_r["O2IMG"][0]}.png'
        match_name = f"{team_1_name} - {team_2_name}"
        match_id = match_r['CI']
        start_at = int(match_r['S'])
        league = match_r["L"]
        league_id = match_r["LI"]
        bookmaker = XbetBookmaker(self._bookmaker_name, match_id, league_id)
        match = Match(match_name, bookmaker, start_at)
        match.general = MatchGeneralInfo(
            MatchTeams([Team(team_1_name, team_1_img), Team(team_2_name, team_2_img)]),
            league, start_at)
        return match

    def get_bets(self, r) -> MatchBets:
        present_bets_in_match = self._get_present_bets_in_match(r)
        bets = []
        for bet in present_bets_in_match:
            try:
                bet_type_id = bet['G']
                bet_name_enum = self._get_key_by_value(self._bet_name_enum_to_id, bet_type_id)
                if bet_name_enum is None:
                    raise ParsingError(f'BetNameEnum does not have the desired value. bet_name_enum:{bet_name_enum}')
                bet_name_enum: BetNameEnum
                coefficients = self._get_coefficients(bet)
                bets.append(Bet(bet_name_enum, coefficients))
            except Exception as e:
                logger.error(e, exc_info=e)
        if len(bets) < 1:
            raise ParsingError('Error bets processing. List of bets are empty')
        return MatchBets(bets)

    @staticmethod
    def _get_key_by_value(dictionary, value) -> Any | None:
        for key, val in dictionary.items():
            if val == value:
                return key
        return None

    @staticmethod
    def _get_coefficients(bet: dict) -> list:
        bet_type_id = int(bet['G'])
        coefficients = []
        if bet_type_id in [1, 8, 19, 101]:
            for b in bet['E']:
                coefficients.append(Coefficient(b[0]['C']))
        elif bet_type_id == 17:
            for i in range(len(bet['E'][0])):
                total = Total(bet['E'][0][i]['P'], bet['E'][0][i]['C'], bet['E'][1][i]['P'])
                coefficients.append(total)
        else:
            raise ParsingError(f'No processing bet_type_id:{bet_type_id}\nbet:\n{bet}')
        return coefficients

    def _get_present_bets_in_match(self, r) -> list:
        bet_type_to_id = self._bet_name_enum_to_id
        bets_in_match = []
        for b in r['Value']['GE']:
            if b['G'] in list(bet_type_to_id.values()):
                bets_in_match.append(b)
        return bets_in_match

    def get_match_result(self, r: dict, bookmaker: XbetBookmaker, general: MatchGeneralInfo) -> MatchResult | None:
        result = None
        for sport in r['sport']:
            for champ in sport['champs']:
                if not champ['id'] == bookmaker.league_id:
                    continue

                for game in champ['games']:
                    teams = general.teams.teams
                    team_1: Team = teams[0]
                    game_team_1_name = game['opp1']
                    game_team_2_name = game['opp2']

                    if not team_1.name == game_team_1_name:
                        continue

                    score = game['score'].split(':', 2)
                    t_1 = TeamResult(game_team_1_name, int(score[0]))
                    t_2 = TeamResult(game_team_2_name, int(score[1].split(' ')[0]))
                    result = MatchResult([t_1, t_2])
                    result.time_score = game['score'].split(' ', 2)[1]

            if result is None:
                continue
            break

        return result
