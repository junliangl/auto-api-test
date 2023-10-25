import sqlite3
import pymysql

from typing import Union, Any, List
from pymysql.cursors import DictCursor
from pymysql.converters import escape_str, escape_item, escape_string, escape_sequence

from common.utils.log import Log
from common.utils.config import config


class ConnectDatabase:
    """
    数据库连接和配置
    """

    __db_name = ""

    @property
    def db_name(self):
        return self.__db_name

    def __init__(self, host=None, port=None, user=None, password=None, db=None, is_sqlite=False):
        if host is None:
            self.__host = config.db_host
        if port is None:
            self.__port = config.db_port
        if user is None:
            self.__user = config.db_user
        if password is None:
            self.__password = config.db_password
        if db is None:
            Log(description=f"db", print_to_file=False, log_path_type="db").log.warn("数据库名字为空!")
        self.__db_name = db
        if is_sqlite:
            self.connect = sqlite3.connect(database=db)
            self.connect.row_factory = sqlite3.Row  # 以字典形式返回数据
            self.cursor = self.connect.cursor()
        else:
            self.connect = pymysql.connect(host=self.__host, port=self.__port,
                                           user=self.__user, password=self.__password, db=db)
            self.cursor = self.connect.cursor(DictCursor)  # 以字典形式返回数据

    def __str__(self):
        return "使用数据库, 包括 sql语句, 关闭数据库"

    def use_db(self, sql: str, data=None, *args, **kwargs) -> Union[tuple[dict[str, Any], ...], dict[str, Any], None]:
        """
        操作数据库
        """
        self.cursor.execute(sql, args)
        self.connect.commit()
        if type(data) is str:
            results = self.cursor.fetchall()
            if isinstance(results, list):
                index = 0
                for result in results:
                    if not isinstance(result, dict):
                        results[index] = dict(result)
                    index += 1
            return results
        if type(data) is int:
            results = self.cursor.fetchmany(data)
            if isinstance(results, list):
                index = 0
                for result in results:
                    if not isinstance(result, dict):
                        results[index] = dict(result)
                    index += 1
            return results
        result = self.cursor.fetchone()
        if result is not None:
            return dict(result)

    def close_db(self):
        """
        关闭数据库连接
        """
        self.cursor.close()
        self.connect.close()

    @staticmethod
    def escape_string(data: str) -> str:
        """
        处理 "" '' 等特殊字符等问题
        """
        return escape_string(data)

    @staticmethod
    def escape_str(data: str) -> str:
        """
        处理格式化字符串 %s 无法识别的问题
        """
        return escape_str(data)

    @classmethod
    def escape_dict(cls, data: dict) -> dict:
        """
        处理字典类型的格式化字符串问题
        """
        for k, v in data.items():
            if type(v) is str:
                if "%" in v:
                    # 处理无法传入 % 符号的问题
                    v = cls.escape_item(v)
                    data[k] = v.replace("%", "%%")
                else:
                    data[k] = cls.escape_item(v)
            elif v is None:
                data[k] = cls.escape_item(v)
        return data

    @staticmethod
    def escape_item(data):
        """
        处理多种数据类型的问题
        """
        return escape_item(data, charset='utf-8')

    @staticmethod
    def escape_sequence(data):
        return escape_sequence(data, charset='utf-8')

    @staticmethod
    def escape_list_str(data: List[str]) -> List[str]:
        """
        处理 iterable 对象的属性中包含 str 类型的情况
        """
        i = 0
        for str_ in data:
            if type(str_) is str:
                data[i] = escape_str(str_)
            i += 1
        return data
