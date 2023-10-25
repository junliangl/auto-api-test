from dataclasses import dataclass, asdict, astuple, is_dataclass

from common.utils.data.json import ProcessJson


@dataclass
class BaseDataClass:

    def serializable_to_dict(self):
        return asdict(self)

    def serializable_to_tuple(self):
        return astuple(self)

    def serializable_to_json(self):
        return ProcessJson.obj_to_json(self.serializable_to_dict())

    def deserializable_by_dict(self, dict_data: dict):
        for attr in dict_data:
            if hasattr(self, str(attr)):
                current = self
                while True:
                    if current.__class__ is BaseDataClass:
                        current = None
                        break
                    if not hasattr(current, "__annotations__"):
                        current = current.__class__.__base__()
                        continue
                    cls = current.__annotations__.get(attr, -1)
                    if is_dataclass(cls):
                        # property: dataclass
                        sub_attr = current.__annotations__[attr]()
                        sub_attr.deserializable_by_dict(dict_data[attr])
                        setattr(self, attr, sub_attr)
                        break
                    elif hasattr(cls, "__args__"):
                        # property: list[dataclass]
                        setattr(self, attr, [])
                        for every_sub_attr in dict_data[attr]:
                            sub_attr = current.__annotations__[attr].__args__[0]()
                            sub_attr.deserializable_by_dict(every_sub_attr)
                            getattr(self, attr).append(sub_attr)
                        break
                    else:
                        current = current.__class__.__base__()
                if not current:
                    # property: int, str, bool, ...
                    setattr(self, attr, dict_data[attr])

    def deserializable_by_tuple(self, tuple_data: tuple):
        raise NotImplementedError

    def deserializable_by_json(self, json_data: str):
        dict_data = ProcessJson.json_to_obj(json_data)
        return self.deserializable_by_dict(dict_data)

    def __str__(self):
        return ProcessJson.obj_to_json(self.serializable_to_dict(), indent=4)
