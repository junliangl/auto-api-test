import random
import string
from typing import Union
from decimal import Decimal, Context, ROUND_HALF_UP


class MathTool:
    """
    处理一些数据的数学工具
    """

    @staticmethod
    def random_int(start=10, end=20):
        return random.randint(start, end)

    @staticmethod
    def random_float(start, end, digit: int):
        return round(random.uniform(start, end), digit)

    @staticmethod
    def random_choice(_iter):
        return random.choice(_iter)

    @staticmethod
    def random_lower_str(count=3):
        """随机小写英文字母"""
        random_str = ""
        for i in range(count):
            random_str += random.choice(string.ascii_lowercase)
        return random_str

    @staticmethod
    def random_upper_str(count=3):
        """随机大写英文字母"""
        random_str = ""
        for i in range(count):
            random_str += random.choice(string.ascii_uppercase)
        return random_str

    @staticmethod
    def random_number_str(count=11):
        """随机字符串数字"""
        random_str = f"{random.randint(1, 9)}"
        for i in range(count - 1):
            random_str += random.choice(string.digits)
        return random_str

    @staticmethod
    def to_decimal(data: Union[str, float, int, Decimal]):
        """
        转换为 decimal 类型
        """
        if isinstance(data, Decimal):
            return data
        elif isinstance(data, str):
            return Decimal(data)
        elif isinstance(data, float):
            return Decimal(str(data))
        elif isinstance(data, int):
            return Decimal(data)

    @staticmethod
    def round(data: Union[Decimal, str, float, int], digit) -> Decimal:
        """
        四舍五入保留小数位置
        """
        data = MathTool.to_decimal(data)
        context = Context(rounding=ROUND_HALF_UP)
        return data.quantize(Decimal(f"1E-{digit}"), context=context)

    @staticmethod
    def max(*args, **kwargs):
        return max(*args, **kwargs)

    @staticmethod
    def min(*args, **kwargs):
        return min(*args, **kwargs)
