from typing import Any

from sqlalchemy.types import JSON

from common.entity.support.type.base_type import BaseType


class JsonType(BaseType):

    impl = JSON

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        # sqlalchemy 优化了 json, 自动转换
        return value

    def process_result_value(self, value: str, dialect):
        # sqlalchemy 优化了 json, 自动转换
        return value

    @property
    def python_type(self):
        return Any
