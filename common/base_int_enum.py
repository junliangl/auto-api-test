from __future__ import annotations
from enum import IntEnum

from common.utils.math_tool import MathTool
from common.exception.param_error import ParamsError
from common.exception.type_error import TypesError


class BaseIntEnum(IntEnum):

    @classmethod
    def members(cls):
        return tuple(cls.__members__.values())

    @classmethod
    def start_ordinal(cls):
        return 0

    @property
    def ordinal(self):
        """
        返回枚举类型的序号
        """

        if not isinstance(self.start_ordinal(), int):
            raise TypesError(self.start_ordinal())
        original_ordinal = self.members().index(self)
        return original_ordinal + self.start_ordinal()

    @classmethod
    def ordinal_to_type(cls, ordinal: int) -> BaseIntEnum:
        """
        根据 ordinal 获取对应的 type
        """

        original_ordinal = ordinal - cls.start_ordinal()
        if not isinstance(original_ordinal, int) or original_ordinal < 0:
            raise ParamsError(ordinal)
        return cls.members()[original_ordinal]

    @classmethod
    def random_type(cls) -> BaseIntEnum:
        """
        返回一个随机的类型
        """

        return MathTool.random_choice(cls.members())
