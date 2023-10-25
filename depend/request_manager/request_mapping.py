from functools import wraps


class RequestMapping:

    @staticmethod
    def url(path: str):
        def add_path(cls):
            cls.path = path
            return cls

        return add_path

    @staticmethod
    def class_mapping(path: str):
        def add_path(cls):
            cls.path = cls.path + path
            return cls

        return add_path

    @staticmethod
    def method_mapping(path: str):
        def wrapper(test_case):
            @wraps(test_case)
            def change_path(*args, **kwargs):
                cls_path = args[0].path
                args[0].path = cls_path + path
                try:
                    test_case(*args, **kwargs)
                finally:
                    args[0].path = cls_path
            return change_path
        return wrapper
