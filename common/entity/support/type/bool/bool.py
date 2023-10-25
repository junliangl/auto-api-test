from sqlalchemy.types import Boolean

from common.exception.param_error import ParamsError
from common.entity.support.type.base_type import BaseType


class BoolType(BaseType):

    impl = Boolean
    cache_ok = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value: bool, dialect):
        if value is None:
            return None
        if not isinstance(value, bool):
            raise ParamsError(f"{value} \nmust be a bool type")
        return value

    def process_result_value(self, value, dialect):
        return bool(value)

    @property
    def python_type(self):
        return bool
