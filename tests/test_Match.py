from unittest.mock import MagicMock
import pytest

from parsing.match.bets.bet import MatchBets
from parsing.match.bookmakers.match_bookmaker import MatchBookmaker
from parsing.match.match import Match
from parsing.match.match_general_info import MatchGeneralInfo
from parsing.match.match_result import MatchResult

match_name = 'Барселона - Реал'


@pytest.fixture
def match_fixture():
    mock_bookmaker = MagicMock(spec=MatchBookmaker)
    mock_general_info = MagicMock(spec=MatchGeneralInfo)
    mock_bets = MagicMock(spec=MatchBets)
    mock_result = MagicMock(spec=MatchResult)
    match = Match(match_name, mock_bookmaker, 1652817600)
    return match, mock_bookmaker, mock_general_info, mock_bets, mock_result


def test_name(match_fixture):
    match, _, _, _, _ = match_fixture
    assert match.name == match_name
    new_match_name = match_name + 'Нов'
    match.name = new_match_name
    assert match.name == new_match_name


def test_bookmaker(match_fixture):
    match, mock_bookmaker, _, _, _ = match_fixture
    assert match.bookmaker == mock_bookmaker
    new_bookmaker = MagicMock(spec=MatchBookmaker)
    match.bookmaker = new_bookmaker
    assert match.bookmaker == new_bookmaker


def test_general(match_fixture):
    match, _, mock_general_info, _, _ = match_fixture
    assert match.general is None
    match.general = mock_general_info
    assert match.general == mock_general_info


def test_bets(match_fixture):
    match, _, _, mock_bets, _ = match_fixture
    assert match.bets is None
    match.bets = mock_bets
    assert match.bets == mock_bets


def test_result(match_fixture):
    match, _, _, _, mock_result = match_fixture
    assert match.result is None
    match.result = mock_result
    assert match.result == mock_result


def test_match_start_date(match_fixture):
    match, _, _, _, _ = match_fixture
    assert match.match_start_date == 1652817600
    match.match_start_date = 1652817601
    assert match.match_start_date == 1652817601


def test_get_attributes_dict(match_fixture):
    match, mock_bookmaker, mock_general_info, mock_bets, mock_result = match_fixture
    mock_bookmaker.get_attributes.return_value = {"bookmaker_attribute": "bookmaker_value"}
    mock_general_info.get_attributes.return_value = {"general_attribute": "general_value"}
    mock_bets.get_attributes.return_value = {"bets_attribute": "bets_value"}
    mock_result.get_attributes.return_value = {"result_attribute": "result_value"}
    expected_dict = {
        'name': match_name,
        'match_start_date': 1652817600,
        'bookmaker': {"bookmaker_attribute": "bookmaker_value"},
        'general': {"general_attribute": "general_value"},
        'bets': {"bets_attribute": "bets_value"},
        'result': {"result_attribute": "result_value"}
    }
    match.general = mock_general_info
    match.bets = mock_bets
    match.result = mock_result
    assert match.get_attributes_dict() == expected_dict
