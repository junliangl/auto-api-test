import time
import datetime
import random

import pytz


class ProcessTime:
    """
    处理日期和时间
    """

    @staticmethod
    def current_datetime(timezone=None):
        """
        获取当前 datetime
        """
        current_time = datetime.datetime.now().replace(microsecond=0)
        if timezone is None:
            return current_time
        else:
            return current_time.astimezone(tz=pytz.timezone(timezone))

    @staticmethod
    def current_str_time(format_="%Y-%m-%d %H:%M:%S", timezone=None):
        """
        获取当前格式化字符串时间
        """
        return ProcessTime.current_datetime(timezone).strftime(format_)

    @staticmethod
    def current_timestamp():
        """
        获取当前时间戳,单位:s
        """
        return int(ProcessTime.current_datetime().timestamp())

    @staticmethod
    def datetime_to_str_time(datetime_obj: datetime.datetime, format_="%Y-%m-%d %H:%M:%S", timezone=None):
        """
        datetime 转化成格式化字符串时间
        """
        if timezone:
            datetime_obj = datetime_obj.astimezone(pytz.timezone(timezone))
        return datetime_obj.strftime(format_)

    @staticmethod
    def datetime_to_timestamp(datetime_obj: datetime.datetime):
        """
        datetime 转化成时间戳,单位:s
        """
        return int(datetime_obj.timestamp())

    @staticmethod
    def str_time_to_datetime(str_time, format_="%Y-%m-%d %H:%M:%S", timezone=None):
        """
        格式化字符串时间转化成 datetime
        """
        to_datetime = datetime.datetime.strptime(str_time, format_).replace(microsecond=0)
        if timezone:
            to_datetime = to_datetime.astimezone(tz=pytz.timezone(timezone))
        return to_datetime

    @staticmethod
    def timestamp_to_datetime(timestamp, timezone=None):
        """
        时间戳转化成 datetime
        """
        to_datetime = datetime.datetime.fromtimestamp(timestamp).replace(microsecond=0)
        if timezone:
            to_datetime = to_datetime.astimezone(tz=pytz.timezone(timezone))
        return to_datetime

    @staticmethod
    def str_time_to_timestamp(str_time, format_="%Y-%m-%d %H:%M:%S"):
        """
        格式化字符串时间转化成时间戳,单位:s
        """
        to_datetime = datetime.datetime.strptime(str_time, format_)
        return to_datetime.timestamp()

    @staticmethod
    def timestamp_to_str_time(timestamp, format_="%Y-%m-%d %H:%M:%S", timezone=None):
        """
        时间戳转化成格式化字符串
        """
        to_datetime = datetime.datetime.fromtimestamp(timestamp)
        if timezone:
            to_datetime = to_datetime.astimezone(tz=pytz.timezone(timezone))
        return to_datetime.strftime(format_)

    @staticmethod
    def random_datetime(start_year: int = 1970, end_year: int = datetime.datetime.now().year):
        """
        返回一个随机的日期: datetime
        """
        year = random.randint(start_year, end_year)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        return datetime.datetime(year, month, day, hour, minute, second)

    @staticmethod
    def random_str_time(start_year: int = 1970, end_year: int = datetime.datetime.now().year,
                        format_="%Y-%m-%d %H:%M:%S"):
        """
        返回一个随机的日期: str_time
        """
        random_datetime = ProcessTime.random_datetime(start_year, end_year)
        return ProcessTime.datetime_to_str_time(random_datetime, format_)

    @staticmethod
    def random_timestamp(start_year: int = 1970, end_year: int = datetime.datetime.now().year):
        """
        返回一个随机的日期: timestamp
        """
        random_datetime = ProcessTime.random_datetime(start_year, end_year)
        return ProcessTime.datetime_to_timestamp(random_datetime)

    @staticmethod
    def to_timedelta(*args, **kwargs):
        """
        获取 timedelta 对象
        """
        return datetime.timedelta(*args, **kwargs)

    @staticmethod
    def is_daylight_saving_time(timezone=None):
        """
        判断是否是夏令时
        """
        return ProcessTime.current_datetime(timezone).dst() != datetime.timedelta(0)

    @staticmethod
    def sleep(seconds=1):
        """
        等待
        """
        time.sleep(seconds)
