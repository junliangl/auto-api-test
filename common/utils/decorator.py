import threading
from functools import wraps
from dataclasses import field

from common.utils.process_time import ProcessTime
from common.utils.log import Log


class Decorator:

    @staticmethod
    def cal_time(func):
        """
        计算函数执行时间
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            start = ProcessTime.current_timestamp()
            func(*args, **kwargs)
            end = ProcessTime.current_timestamp()
            print(end - start)

        return wrapper

    @staticmethod
    def const_single(cls):
        """
        一致性单例模式
        """
        instance = None

        def wrapper(*args, **kwargs):
            nonlocal instance
            if instance is None:
                instance = super(cls, cls).__new__(cls)
            return instance

        cls.__new__ = wrapper
        return cls

    @staticmethod
    def safe_const_single(cls):
        """
        线程安全的一致性单例模式
        """
        instance = None
        lock = threading.Lock()

        def wrapper(*args, **kwargs):
            nonlocal instance
            if instance is None:
                with lock:
                    if instance is None:
                        instance = super(cls, cls).__new__(cls)
            return instance

        cls.__new__ = wrapper
        return cls

    @staticmethod
    def limit_single(cls):
        """
        限制性单例模式
        """
        instances = {}

        def wrapper(*args, **kwargs):
            nonlocal instances
            key = (args, frozenset(kwargs.items()))
            if key not in instances:
                instances[key] = super(cls, cls).__new__(cls)
            return instances[key]

        cls.__new__ = wrapper
        return cls

    @staticmethod
    def safe_limit_single(cls):
        """
        线程安全的限制性单例模式
        """
        instances = {}
        lock = threading.Lock()

        def wrapper(*args, **kwargs):
            nonlocal instances
            key = (args, frozenset(kwargs.items()))
            if key not in instances:
                with lock:
                    if key not in instances:
                        instances[key] = super(cls, cls).__new__(cls)
            return instances[key]

        cls.__new__ = wrapper
        return cls

    @staticmethod
    def log(cls):
        """
        日志装饰器
        """

        cls.log = Log(f"{cls.__name__}").log
        return cls

    @staticmethod
    def default_data(cls):
        for attr in cls.__annotations__:
            setattr(cls, attr, field(default=None))
        return cls
