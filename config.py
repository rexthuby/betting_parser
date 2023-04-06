from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class Proxy:
    ip: str
    username: str
    password: str
    http_port: int
    socks5_port: int


@dataclass
class Config:
    db: DbConfig
    proxy: Proxy


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        proxy=Proxy(
            ip=env.str('PROXY_ID'),
            username=env.str('PROXY_USERNAME'),
            password=env.str('PROXY_PASSWORD'),
            http_port=env.int('PROXY_HTTP_PORT'),
            socks5_port=env.int('PROXY_SOCKS5_PORT') if not None else ''
        )
    )


config = load_config(".testenv")
