from configparser import ConfigParser

from common.path import DB_CONFIG_PATH, HTTP_CONFIG_PATH
from common.utils.decorator import Decorator
from common.utils.cache import cache


@Decorator.const_single
class Config:

    def __init__(self):
        self.read_config = ConfigParser()

    @property
    @cache(1000, 60 * 10)
    def db(self):
        self.read_config.read(DB_CONFIG_PATH)
        return self.read_config.get("database", "db")

    @property
    @cache(1000, 60 * 10)
    def db_host(self):
        self.read_config.read(DB_CONFIG_PATH)
        return self.read_config.get("database", "host")

    @property
    @cache(1000, 60 * 10)
    def db_port(self):
        self.read_config.read(DB_CONFIG_PATH)
        return int(self.read_config.get("database", "port"))

    @property
    @cache(1000, 60 * 10)
    def db_user(self):
        self.read_config.read(DB_CONFIG_PATH)
        return self.read_config.get("database", "user")

    @property
    @cache(1000, 60 * 10)
    def db_password(self):
        self.read_config.read(DB_CONFIG_PATH)
        return self.read_config.get("database", "password")

    @property
    @cache(1000, 60 * 10)
    def db_relation(self):
        self.read_config.read(DB_CONFIG_PATH)
        return self.read_config.get("database", "relation")

    @property
    @cache(1000, 60 * 10)
    def is_echo_sql(self):
        self.read_config.read(DB_CONFIG_PATH)
        return self.read_config.get("database", "is_echo_sql") == "true"

    @property
    @cache(1000, 60 * 10)
    def db_pool_size(self):
        self.read_config.read(DB_CONFIG_PATH)
        return int(self.read_config.get("database", "pool_size"))

    @property
    @cache(1000, 60 * 10)
    def db_max_overflow(self):
        self.read_config.read(DB_CONFIG_PATH)
        return int(self.read_config.get("database", "max_overflow"))

    @property
    @cache(1000, 60 * 10)
    def demo_db_name(self):
        self.read_config.read(DB_CONFIG_PATH)
        return self.read_config.get("database", "demo_db_name")

    @property
    @cache(1000, 60 * 10)
    def http_protocol(self):
        self.read_config.read(HTTP_CONFIG_PATH)
        return self.read_config.get("http", "protocol")

    @property
    @cache(1000, 60 * 10)
    def http_host(self):
        self.read_config.read(HTTP_CONFIG_PATH)
        return self.read_config.get("http", "host")

    @property
    @cache(1000, 60 * 10)
    def http_port(self):
        self.read_config.read(HTTP_CONFIG_PATH)
        return self.read_config.get("http", "port")


config = Config()
