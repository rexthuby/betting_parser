import asyncio
import aiohttp
from aiohttp import BasicAuth, ContentTypeError
from config import SportEnum
from custom_exception.ParsingError import ParsingError
from custom_exception.RequestError import RequestError
from misc.logger import logger
from parsing.BaseBookmakerParser import BaseBookmakerParser
from parsing.XbetParsedDataHandler import XbetParsedDataHandler
from parsing.match.bets.bet import MatchBets
from parsing.match.match import Match
from parsing.match.match_result import MatchResult, TeamResult


class XbetParser(BaseBookmakerParser):
    def __init__(self, parsed_data_handler: XbetParsedDataHandler = XbetParsedDataHandler()):
        super().__init__(parsed_data_handler)

    async def get_matches(self, sport: SportEnum) -> list[Match]:
        sport_name_id = {SportEnum.football.value: 1, SportEnum.ice_hockey.value: 2}
        sport_id = sport_name_id[sport.value]
        url = f'https://1xbet.com/LineFeed/Get1x2_VZip?sports={sport_id}' \
              f'&count=50&tf=2200000&mode=4&getEmpty=true'
        async with aiohttp.ClientSession(headers=self._header) as session:
            try:
                for n in range(5):
                    async with session.get(url, proxy=self._proxy, proxy_auth=self._proxy_auth) as response:
                        try:
                            res: dict = await response.json()
                        except ContentTypeError:
                            await asyncio.sleep(0.4)
                        else:
                            handler: XbetParsedDataHandler = self._parsed_data_handler
                            return handler.get_matches(res)
                raise RequestError('Failed to connect to 1xbet')
            finally:
                await session.close()

    async def get_match_bets(self, match_id: int) -> MatchBets:
        url = f'https://1xbet.com/LineFeed/GetGameZip?id={match_id}&lng=ru&cfview=0&isSubGames=true&' \
              f'GroupEvents=true&allEventsGroupSubGames=true&countevents=250&marketType=1&isNewBuilder=true'
        async with aiohttp.ClientSession(headers=self._header) as session:
            try:
                for n in range(5):
                    async with session.get(url, proxy=self._proxy, proxy_auth=self._proxy_auth) as response:
                        try:
                            r: dict = await response.json()
                        except ContentTypeError:
                            await asyncio.sleep(0.4)
                        else:
                            handler: XbetParsedDataHandler = self._parsed_data_handler
                            return handler.get_bets(r)
                raise RequestError('Failed to connect to 1xbet')
            finally:
                await session.close()

    async def get_match_result_url_part(self, game_id: int) -> str | None:
        url = f'https://1xbet.com/SiteService/StatisticStatuses?constId={game_id}'
        async with aiohttp.ClientSession(headers=self._header) as session:
            try:
                for n in range(5):
                    async with session.get(url, proxy=self._proxy, proxy_auth=self._proxy_auth) as response:
                        try:
                            r: dict = await response.json()
                        except ContentTypeError:
                            await asyncio.sleep(0.4)
                        else:
                            return r['I']
                raise RequestError('Failed to connect to 1xbet')
            finally:
                await session.close()

    async def get_match_result(self, match_result_url_part: str) -> MatchResult | None:
        link = f'https://eventsstat.com/statisticpopup/game/1/{match_result_url_part}/main?ln=ru'
        async with aiohttp.ClientSession(headers=self._header) as session:
            try:
                for n in range(5):
                    async with session.get(link, proxy=self._proxy, proxy_auth=self._proxy_auth) as response:
                        try:
                            r = await response.text()
                        except ContentTypeError:
                            await asyncio.sleep(0.4)
                        else:
                            try:
                                handler: XbetParsedDataHandler = self._parsed_data_handler
                                return handler.get_match_result(r)
                            except ParsingError:
                                continue
                raise RequestError('Failed to connect to 1xbet')
            finally:
                await session.close()
