from enum import Enum

from sqlalchemy.types import Integer

from common.entity.support.type.enum.base_enum_type import BaseEnumType


class EnumOrdinalType(BaseEnumType):

    impl = Integer
    cache_ok = True

    def process_bind_param(self, value: Enum, dialect):
        if value is None:
            return None
        return value.ordinal

    def process_result_value(self, value: int, dialect):
        if value is None:
            return None
        return self.enum_class.ordinal_to_type(value)
