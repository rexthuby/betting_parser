import asyncpg
from asyncpg import Connection

from config import config
from misc.logger import logger


class BaseModel:
    _db_config = config.db

    def __init__(self):
        self._connect = None


    async def _get_connection(self) -> Connection:
        db_conf = self._db_config
        return await asyncpg.connect(user=db_conf.user, password=db_conf.password,
                                     host=db_conf.host, database=db_conf.database)

    def _connection_decorator(func):
        async def wrapper(self, query, *args):
            try:
                self._connect = await self._get_connection()
            except Exception as e:
                logger.error(e, exc_info=e)
                raise Exception('Не получилось подключиться к базе данных')
            else:
                try:
                    return await func(self, query, *args)
                except Exception as e:
                    logger.error(e, exc_info=e)
                    raise Exception('Не удалось получить значиния с БД')
                finally:
                    await self._connect.close()
                    self._connect = None

        return wrapper

    _connection_decorator = staticmethod(_connection_decorator)
