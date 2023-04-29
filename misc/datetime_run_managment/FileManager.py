import os

from misc.datetime_run_managment.KeyValueManagerInterface import KeyValueManagerInterface
from misc.datetime_run_managment.FileKeyError import FileKeyError


class FileManager(KeyValueManagerInterface):
    def __init__(self, file_path: str):
        self._file_path = file_path

    def save_or_update_key(self, key: str, value: str):
        self._create_file_if_not_exists(self._file_path)
        updated = False
        with open(self._file_path, 'r') as f:
            lines = f.readlines()
        with open(self._file_path, 'w') as f:
            for line in lines:
                if line.startswith(key + '='):
                    f.write(f"{key}={value}\n")
                    updated = True
                    break
                else:
                    f.write(line)
            if not updated:
                f.write(f"{key}={value}\n")

    def get_value(self, key: str):
        self._create_file_if_not_exists(self._file_path)
        with open(self._file_path, 'r') as f:
            for line in f:
                if line.startswith(key + '='):
                    return line.strip().split('=')[1]
        raise FileKeyError()

    def _create_file_if_not_exists(self, file_path):
        if not os.path.exists(file_path):
            with open(file_path, 'w'):
                pass