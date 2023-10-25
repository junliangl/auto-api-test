from typing import List

from sqlalchemy.types import JSON

from common.entity.support.type.json.json import JsonType


class ListJsonType(JsonType):

    impl = JSON

    @property
    def python_type(self):
        return List
