import asyncio
import logging

import asyncpg
import config as conf

config = conf.config
logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
)


async def create_db():
    try:
        conn: asyncpg.Connection = await asyncpg.connect(user=config.db.user, password=config.db.password,
                                                         host=config.db.host, database=config.db.database)
        logger.info('Connect to db')
        try:
            await conn.execute(open('create_db.sql', 'r', encoding='utf-8').read())
            logger.info('Database operation successful')
        except Exception as error:
            logger.error(error)
        finally:
            await conn.close()
    except Exception as error:
        logger.error(f"Bot can not connect to database: {error}")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())
