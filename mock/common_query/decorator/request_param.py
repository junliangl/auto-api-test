from typing import Type
from functools import wraps

from flask import request

from common.base_data_class import BaseDataClass


def request_param(param_name: str, serializable_class: Type[BaseDataClass]):
    def wrapper(server):
        @wraps(server)
        def make_param(*args, **kwargs):
            param = serializable_class()
            param.deserializable_by_dict(request.json)
            kwargs[param_name] = param
            return server(*args, **kwargs)

        return make_param

    return wrapper
