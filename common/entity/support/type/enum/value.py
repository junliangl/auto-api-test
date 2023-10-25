from enum import Enum

from sqlalchemy.types import UserDefinedType

from common.entity.support.type.enum.base_enum_type import BaseEnumType


class EnumValueType(BaseEnumType):

    impl = UserDefinedType
    cache_ok = True

    def process_bind_param(self, value: Enum, dialect):
        if value is None:
            return None
        return value.value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return self.enum_class(value)
