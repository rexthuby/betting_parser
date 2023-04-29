import pytest
from unittest.mock import AsyncMock

from unittest.mock import MagicMock
from datetime import datetime

from parsing.XbetParsedDataHandler import XbetParsedDataHandler
from parsing.XbetParser import XbetParser
from parsing.match.match import Match


@pytest.fixture
def mock_parser():
    data_handler = MagicMock(spec=XbetParsedDataHandler)
    parser = XbetParser()
    match = MagicMock(spec=Match)
    parser.get_matches.return_value = [match]
    parser.get_match_bets.return_value = []
    parser.get_match_result.return_value = None
    parser.get_match_result_url_part.return_value = ''
    return parser


@pytest.fixture
def mock_match_model():
    match_model = MagicMock()
    match_model.insert_match_without_result.return_value = 1
    match_model.get_all_by_id.return_value = {'id': 1, 'bookmaker': {}, 'start_at': datetime.now().timestamp()}
    return match_model


@pytest.fixture
def mock_scheduler():
    scheduler = MagicMock()
    return scheduler
