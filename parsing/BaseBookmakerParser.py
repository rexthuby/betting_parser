from typing import TypeVar

import fake_useragent
from aiohttp import BasicAuth

from config import config
from parsing.BaseParsedDataHandler import base_parsed_data_handler


class BaseBookmakerParser:
    _user = fake_useragent.UserAgent().random
    _header = {'user-agent': _user}
    _config = config
    _proxy = f"http://{_config.proxy.ip}:{_config.proxy.http_port}"
    _proxy_auth = BasicAuth(_config.proxy.username, _config.proxy.password)

    def __init__(self, parsed_data_handler: base_parsed_data_handler):
        self._parsed_data_handler = parsed_data_handler


base_parser = TypeVar('base_parser', bound=BaseBookmakerParser)
