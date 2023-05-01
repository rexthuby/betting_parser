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
                if 'хозяев' in match_r["O1"].lower() or 'хозяев' in match_r["O2"].lower():
                    continue
                match = self._prepare_match(match_r)
                matches.append(match)
            except Exception as e:
                logger.error('Не правильная обработка данных от 1xber', exc_info=e)
        if len(matches) < 1:
            raise ParsingError('Масив матчей пуст')
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
        bookmaker = XbetBookmaker(self._bookmaker_name, match_id)
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
                    raise ParsingError('В BetNameEnum нет нужного значения value')
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
            raise ParsingError(f'Нет обработки bet_type_id:{bet_type_id}\nbet:\n{bet}')
        return coefficients

    def _get_present_bets_in_match(self, r) -> list:
        bet_type_to_id = self._bet_name_enum_to_id
        bets_in_match = []
        for b in r['Value']['GE']:
            if b['G'] in list(bet_type_to_id.values()):
                bets_in_match.append(b)
        return bets_in_match

    def get_match_result(self, r) -> MatchResult | None:
        soup = BeautifulSoup(r, 'lxml')
        all_li_info_div = soup.find(class_='old-sections old-layout__sections')
        if all_li_info_div is None:
            return None
        if self._check_match_end(soup) is False:
            return None
        base_table = all_li_info_div.find(class_='old-sections__item js-item-2')
        table_body: Tag = base_table.tbody
        all_tr_list = table_body.find_all('tr')
        tr_list: list[Tag] = [all_tr_list[1], all_tr_list[2]]
        team_results = []
        for tr in tr_list:
            tr: Tag
            all_td = tr.find_all('td')
            team_name = all_td[0].span.get_text().strip()
            team_score = int(all_td[1].span.get_text().strip())
            team_results.append(TeamResult(team_name, team_score))
        return MatchResult(team_results)

    @staticmethod
    def _check_match_end(soup: BeautifulSoup) -> bool:
        scoreboard = soup.find(class_='old-scoreboard old-layout__scoreboard old-scoreboard--big')
        if scoreboard is None:
            return False
        score_info = scoreboard.find(
            class_='old-scoreboard__info old-scoreboard__info--main old-scoreboard-info old-scoreboard-info--main')
        match_status_div = score_info.find(
            class_='old-scoreboard-info__item')
        if match_status_div is None:
            return False
        match_status = match_status_div.get_text().strip()
        if match_status == 'Матч состоялся':
            return True
        return False
