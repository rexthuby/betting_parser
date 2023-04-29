import pytest
from misc.datetime_run_managment.FileManager import FileManager, FileKeyError


def test_save_or_update_key(tmp_path):
    file_path = tmp_path / "testfile.txt"
    file_contents = "key1=value1\nkey2=value2\n"
    with open(file_path, "w") as f:
        f.write(file_contents)

    manager = FileManager(str(file_path))
    manager.save_or_update_key("key3", "value3")

    with open(file_path, "r") as f:
        updated_contents = f.read()

    expected_contents = "key1=value1\nkey2=value2\nkey3=value3\n"
    assert updated_contents == expected_contents


def test_get_value(tmp_path):
    file_path = tmp_path / "testfile.txt"
    file_contents = "key1=value1\nkey2=value2\n"
    with open(file_path, "w") as f:
        f.write(file_contents)

    manager = FileManager(str(file_path))

    # Test getting an existing value
    assert manager.get_value("key1") == "value1"

    # Test getting a nonexistent value
    with pytest.raises(FileKeyError):
        manager.get_value("key3")
