import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from misc.datetime_run_managment.FileManager import FileManager
from misc.datetime_run_managment.ScriptRun import ScriptRun
from misc.logger import logger


@pytest.fixture
def mock_file_manager():
    return MagicMock(spec=FileManager)


def test_get_last_run_with_valid_date(mock_file_manager):
    # Arrange
    date_str = '2022-01-01 00:00:00'
    mock_file_manager.get_value.return_value = date_str
    script_run = ScriptRun(mock_file_manager)

    # Act
    result = script_run.get_last_run()

    # Assert
    assert result == datetime.strptime(date_str, script_run.LAST_RUN_VALUE_FORMAT)


def test_get_last_run_with_none_value(mock_file_manager):
    # Arrange
    mock_file_manager.get_value.return_value = None
    script_run = ScriptRun(mock_file_manager)

    # Act
    result = script_run.get_last_run()

    # Assert
    assert result is None


def test_get_next_run_with_valid_date():
    # Arrange
    last_run_datetime = datetime(2022, 1, 1, 0, 0)
    script_run = ScriptRun()
    script_run.get_last_run = MagicMock(return_value=last_run_datetime)

    # Act
    result = script_run.get_next_run()

    # Assert
    assert result == last_run_datetime + timedelta(seconds=script_run.SECONDS_PER_RUN)


def test_get_next_run_with_none_value():
    # Arrange
    script_run = ScriptRun()
    script_run.get_last_run = MagicMock(return_value=None)

    # Act
    result = script_run.get_next_run()

    # Assert
    assert result is None


def test_set_last_run(mock_file_manager):
    # Arrange
    last_run_datetime = datetime(2022, 1, 1, 0, 0)
    script_run = ScriptRun(mock_file_manager)

    # Act
    result = script_run.set_last_run(last_run_datetime)

    # Assert
    assert result == datetime(2022, 1, 1, 0, 0)
    mock_file_manager.save_or_update_key.assert_called_once_with(script_run.LAST_RUN_KEY, '2022-01-01 00:00:00')
