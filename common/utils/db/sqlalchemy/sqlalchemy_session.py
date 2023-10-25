from typing import Union, Dict, List, Any

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from common.exception.param_error import ParamsError
from common.utils.config import config
from common.utils.decorator import Decorator


@Decorator.log
@Decorator.limit_single
class SqlalchemySession:
    """
    sqlalchemy 的数据库连接
    """

    @classmethod
    def demo_db(cls, *args, **kwargs):
        return cls(db_name=config.demo_db_name, *args, **kwargs)

    def __init__(self, db=None, relation=None, host=None, port=None, username=None, password=None, db_name=None,
                 is_echo_sql=None, pool_size=None, max_overflow=None, read_config=True):
        if read_config:
            self.db = config.db
            self.relation = config.db_relation
            self.host = config.db_host
            self.port = config.db_port
            self.username = config.db_user
            self.password = config.db_password
            if db_name is None:
                self.log.error("数据库名字为空!")
                raise ParamsError(f"db_name:{db_name}")
            else:
                self.db_name = db_name
            self.is_echo_sql = config.is_echo_sql
            self.pool_size = config.db_pool_size
            self.max_overflow = config.db_max_overflow
        else:
            self.db = db if db is not None else config.db
            self.relation = relation if relation is not None else config.db_relation
            self.host = host if host is not None else config.db_host
            self.port = port if port is not None else config.db_port
            self.username = username if username is not None else config.db_user
            self.password = password if password is not None else config.db_password
            if db_name is None:
                self.log.error("数据库名字为空!")
                raise ParamsError(f"db_name:{db_name}")
            else:
                self.db_name = db_name
            self.is_echo_sql = is_echo_sql if is_echo_sql is not None else config.is_echo_sql
            self.pool_size = pool_size if pool_size is not None else config.db_pool_size
            self.max_overflow = max_overflow if max_overflow is not None else config.db_max_overflow
        self.engine = create_engine(
            f"{self.db}+{self.relation}://{self.username}:{self.password}@{self.host}:{self.port}"
            f"/{self.db_name}", echo=self.is_echo_sql, pool_size=self.pool_size,
            max_overflow=self.max_overflow)
        self.session = Session(self.engine)

    def execute(self, sql: str, *args):
        """
        执行原生 sql
        """
        with self.engine.connect() as con:
            result = con.execute(text(sql), *args)
            con.commit()
        return result

    def fetch_one(self, sql: str, *args) -> Union[Dict[str, Any], None]:
        """
        执行原生 sql 获取第一条数据
        """
        result = self.execute(sql, *args)
        if not result.returns_rows:
            return None
        row = result.fetchone()
        if row is not None:
            columns = result.keys()
            return dict(zip(columns, row))
        else:
            return None

    def fetch_many(self, sql: str, size: int, *args) -> List[Dict[str, Any]]:
        """
        执行原生 sql 获取多条数据
        """
        result = self.execute(sql, *args)
        if not result.returns_rows:
            return []
        rows = result.fetchmany(size)
        if rows:
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
        else:
            return []

    def fetch_all(self, sql: str, *args) -> List[Dict[str, Any]]:
        """
        执行原生 sql 获取所有数据
        """
        result = self.execute(sql, *args)
        if not result.returns_rows:
            return []
        rows = result.fetchall()
        if rows:
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
        else:
            return []
