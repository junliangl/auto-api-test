import re
from abc import ABCMeta
from dataclasses import dataclass
from logging import Logger

from common.base_data_class import BaseDataClass
from common.utils.decorator import Decorator


@Decorator.log
class BaseTestClass(metaclass=ABCMeta):

    path: str
    log: Logger

    @dataclass
    class BaseRequestView(BaseDataClass):
        pass

    @dataclass
    class BaseResponseView(BaseDataClass):
        pass

    def format_path(self, **params):
        path = self.path
        matches = re.findall(r"\{([^}]*)\}", path)
        for match in matches:
            path = path.replace("{" + match + "}", str(params.get(match, "")))
        return path
