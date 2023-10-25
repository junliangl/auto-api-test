from enum import Enum

from sqlalchemy.types import String

from common.entity.support.type.enum.base_enum_type import BaseEnumType


class EnumNameType(BaseEnumType):

    impl = String
    cache_ok = True

    def process_bind_param(self, value: Enum, dialect):
        if value is None:
            return None
        return value.name

    def process_result_value(self, value: str, dialect):
        if value is None:
            return None
        return self.enum_class[value]
