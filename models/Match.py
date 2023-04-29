import json
from typing import TypeVar

import asyncpg
from asyncpg import Connection

from models.BaseModel import BaseModel
from parsing.match.bookmakers.match_bookmaker import MatchBookmaker, BookmakerNameEnum
from parsing.match.match import Match as M
from parsing.match.match_result import MatchResult


class Match(BaseModel):

    @BaseModel._connection_decorator
    async def insert_match_without_result(self, match: M) -> int:
        """
        :return: id of inserted match
        """
        conn: Connection = self._connect
        query = "INSERT INTO matches(name, bookmaker_name, start_at, bookmaker, bets, general)" \
                " VALUES ($1, $2, $3, $4, $5, $6) RETURNING id"
        name = match.name
        bookmaker_name_enum: BookmakerNameEnum = match.bookmaker.name
        bookmaker_name = bookmaker_name_enum.value
        start_at = match.match_start_date
        bookmaker = json.dumps(match.bookmaker.get_attributes())
        bets = json.dumps(match.bets.get_attributes()).encode('utf-8').decode('unicode-escape')
        general = json.dumps(match.general.get_attributes()).encode('utf-8').decode('unicode-escape')
        match_id = int(await conn.fetchval(query, name, bookmaker_name, start_at, bookmaker, bets, general))
        return match_id

    @BaseModel._connection_decorator
    async def update_result(self, match_id: int, match_result: MatchResult):
        """
        :return: status of last SQL command
        """
        result = json.dumps(match_result.get_attributes()).encode('utf-8').decode('unicode-escape')
        conn: Connection = self._connect
        query = "UPDATE matches SET result = $1 WHERE id = $2"
        await conn.execute(query, result, match_id)

    @BaseModel._connection_decorator
    async def get_all_by_id(self, id: int) -> asyncpg.Record:
        conn: Connection = self._connect
        query = "SELECT * FROM matches WHERE id = $1"
        result = await conn.fetch(query, id)
        return result[0]

    @BaseModel._connection_decorator
    async def update_bookmaker(self, match_id: int, bookmaker: MatchBookmaker):
        """
        :return: updated bookmaker
        """
        bookmaker = json.dumps(bookmaker.get_attributes())
        conn: Connection = self._connect
        query = "UPDATE matches SET bookmaker = $1 WHERE id = $2"
        await conn.fetchval(query, bookmaker, match_id)


match_model = TypeVar('match_model', bound=Match)
