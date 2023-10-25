import json
from typing import Any, IO


class ProcessJson:

    @staticmethod
    def json_to_obj(json_obj: str) -> Any:
        return json.loads(json_obj)

    @staticmethod
    def obj_to_json(obj: Any, indent=None) -> str:
        return json.dumps(obj, indent=indent)

    @staticmethod
    def jsonfile_to_obj(jsonfile: IO) -> Any:
        return json.load(jsonfile)

    @staticmethod
    def obj_to_jsonfile(obj: Any, jsonfile: IO):
        json.dump(obj, jsonfile)
