from abc import abstractmethod
from enum import Enum, EnumMeta

from common.exception.param_error import ParamsError
from common.entity.support.type.base_type import BaseType


class BaseEnumType(BaseType):

    def __init__(self, enum_class: EnumMeta, *args, **kwargs):
        if not isinstance(enum_class, EnumMeta):
            raise ParamsError("enum_class must be a EnumMeta")
        self.enum_class = enum_class
        super().__init__(*args, **kwargs)

    @abstractmethod
    def process_bind_param(self, value: Enum, dialect):
        pass

    @abstractmethod
    def process_result_value(self, value, dialect):
        pass

    @property
    def python_type(self):
        return Enum
