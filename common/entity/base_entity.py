from typing import List, Tuple, Iterable, Optional, TypeVar, Union
from abc import abstractmethod
from datetime import date, datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import inspect, Table, and_, or_
from sqlalchemy.util import deprecated

from common.exception.param_error import ParamsError
from common.utils.data.json import ProcessJson
from common.utils.math_tool import MathTool
from common.utils.process_time import ProcessTime
from common.utils.db.sqlalchemy.sqlalchemy_session import SqlalchemySession


class BaseEntity:
    __EntityType = TypeVar("__EntityType", bound="BaseEntity")

    __json_serializable_obj = [date, datetime, Decimal, Enum]

    __connect_ = None
    __engine_ = None
    __session_ = None

    @property
    def __connect(self):
        """
        当前 entity 的数据库连接
        """
        if self.__connect_ is None:
            self.__connect_ = SqlalchemySession(db_name=self.db_name)
        return self.__connect_

    @property
    def engine(self):
        """
        当前 entity 对于数据库的 engine 连接
        """
        if self.__engine_ is None:
            self.__engine_ = self.__connect.engine
        return self.__engine_

    @property
    def session(self):
        """
        当前 entity 对于数据库的 session 连接
        """
        if self.__session_ is None:
            self.__session_ = self.__connect.session
        return self.__session_

    @property
    @abstractmethod
    def db_name(self):
        """
        必须重写当前表所属的 db 的 name, 它决定着 engine 连接的数据库
        example: return "example_db_name"
        """
        pass

    @property
    def table(self) -> Table:
        """
        当前 entity 所属 table 对象
        """
        return self.__table__

    @property
    def module(self):
        """
        当前 entity 所属的表
        """
        return self.__class__

    @property
    def primary_keys(self):
        """
        当前 entity 所属表的 primary key dict
        """
        primary_keys = {}
        for primary_key in self.table.primary_key.columns.keys():
            try:
                primary_keys[primary_key] = getattr(self, primary_key)
            except AttributeError:
                for field in inspect(self).attrs.keys():
                    if getattr(self.__class__, field).primary_key:
                        primary_keys[field] = getattr(self, field)
                        break

        return primary_keys

    def new_entity(self: __EntityType) -> __EntityType:
        """
        当前 entity 的全新的实例
        """
        return self.module()

    @property
    def query(self):
        """
        当前 entity 的 query 对象
        """
        return self.session.query(self.module)

    def find_by_id(self: __EntityType, primary_key=None, auto_commit=True) -> Optional[__EntityType]:
        """
        根据当前 entity 所属表的 primary key 查询数据
        """
        if auto_commit:
            self.session.commit()
        if primary_key:
            return self.query.get(primary_key)
        if any(getattr(self, primary_key) is None for primary_key in self.primary_keys):
            raise ParamsError(f"primary_key contains None: {self.primary_keys}")
        return self.query.filter_by(**self.primary_keys).first()

    def find_by_ids(self: __EntityType, *ids: Union[tuple[int, ...], tuple[str, ...], int, str], autocommit=True) -> \
            Optional[list[__EntityType]]:
        """
        根据当前 entity 所属表的多组 primary key 查询数据
        """
        if autocommit:
            self.session.commit()
        if any(id_ is None for id_ in ids):
            raise ParamsError(f"primary_key contains None: {ids}")
        if len(self.primary_keys) == 1:
            return self.query.filter(getattr(self.module, list(self.primary_keys)[0]).in_(ids)).all()
        else:
            if any(not isinstance(id_, tuple) for id_ in ids):
                raise ParamsError(f"every ids must be tuple: {ids}")
            if any(len(id_) != len(self.primary_keys) for id_ in ids):
                raise ParamsError(f"the number of primary_key is not matched the {ids} number")
            conditions = [getattr(self.module, key).in_(values)
                          for key, values in zip(tuple(self.primary_keys), tuple(zip(*ids)))]
            return self.query.filter(and_(*conditions)).all()

    @deprecated(version="1.0", message="primary key is must ID, please overwrite find_by_id method.")
    def find_by_ID(self):
        return self.query.filter_by(ID=self.ID).first()

    def find_all(self: __EntityType, auto_commit=True) -> Optional[List[__EntityType]]:
        """
        查询当前表的所有数据
        """
        if auto_commit:
            self.session.commit()
        return self.query.all()

    def find_one_by_fields(self: __EntityType, auto_commit=True, **fields) -> Optional[__EntityType]:
        if auto_commit:
            self.session.commit()
        return self.query.filter_by(**fields).first()

    def find_many_by_fields(self: __EntityType, count: int, /, auto_commit=True, **fields) -> \
            Optional[List[__EntityType]]:
        if auto_commit:
            self.session.commit()
        return self.query.filter_by(**fields).limit(count).all()

    def find_all_by_fields(self: __EntityType, auto_commit=True, **fields) -> Optional[List[__EntityType]]:
        if auto_commit:
            self.session.commit()
        return self.query.filter_by(**fields).all()

    def find_all_in_fields(self: __EntityType, auto_commit=True, **fields: dict[str: Iterable]) -> \
            Optional[List[__EntityType]]:
        if auto_commit:
            self.session.commit()
        conditions = [getattr(self.module, field_name).in_(field_values) for field_name, field_values in fields.items()]
        return self.query.filter(and_(*conditions)).all()

    def delete_by_id(self):
        """
        根据当前 entity 所属表的 primary key 删除数据
        """
        if any(getattr(self, primary_key) is None for primary_key in self.primary_keys):
            raise ParamsError(f"primary_key contains None: {self.primary_keys}")
        self.query.filter_by(**self.primary_keys).delete()
        self.session.commit()

    def delete_by_ids(self, *ids: Union[Tuple[int, str], int, str]):
        """
        根据当前 entity 所属表的多个 primary key 删除数据
        """
        if any(id_ is None for id_ in ids):
            raise ParamsError(f"primary_key contains None: {ids}")
        if len(self.primary_keys) == 1:
            self.query.filter(getattr(self.module, list(self.primary_keys)[0]).in_(ids)).delete()
        else:
            if any(not isinstance(id_, tuple) for id_ in ids):
                raise ParamsError(f"every ids must be tuple: {ids}")
            if any(len(id_) != len(self.primary_keys) for id_ in ids):
                raise ParamsError(f"the number of primary_key is not matched the {ids} number")
            conditions = [getattr(self.module, key).in_(values)
                          for key, values in zip(tuple(self.primary_keys), tuple(zip(*ids)))]
            self.query.filter(and_(*conditions)).delete()
        self.session.commit()

    @deprecated(version="1.0", message="primary key is must ID, please overwrite delete_by_id method.")
    def delete_by_ID(self):
        self.query.filter_by(ID=self.ID).delete()
        self.session.commit()

    def delete_all(self: __EntityType, entities: Optional[Iterable[__EntityType]] = None):
        if entities is None:
            self.query.delete()
        else:
            if len(self.primary_keys) == 1:
                self.delete_by_ids(*[tuple(entity.primary_keys.values())[0] for entity in entities])
            else:
                self.delete_by_ids(*[tuple(entity.primary_keys.values()) for entity in entities])
        self.session.commit()

    def delete_all_by_fields(self, **fields):
        self.query.filter_by(**fields).delete()
        self.session.commit()

    def delete_all_in_fields(self, **fields: dict[str: Iterable]):
        conditions = [getattr(self.module, field_name).in_(field_values) for field_name, field_values in fields.items()]
        self.query.filter(and_(*conditions)).delete()
        self.session.commit()

    def delete_any_in_fields(self, **fields: dict[str: Iterable]):
        conditions = [getattr(self.module, field_name).in_(field_values) for field_name, field_values in fields.items()]
        self.query.filter(or_(*conditions)).delete()
        self.session.commit()

    def save(self):
        """
        保存当前 entity
        """
        self.session.add(self)
        self.session.commit()

    def save_all(self: __EntityType, entities: Iterable[__EntityType]):
        """
        保存多个 entities
        """
        self.session.add_all(entities)
        self.session.commit()

    def update(self):
        """
        根据 primary key 更新当前 entity
        """
        self.session.merge(self)
        self.session.commit()

    def refresh(self, auto_commit=True):
        """
        刷新当前 entity
        """
        if auto_commit:
            self.session.commit()
        self.session.refresh(self)

    @abstractmethod
    def init(self):
        """
        初始化当前 entity
        """
        pass

    @property
    def math_processor(self):
        return MathTool

    @property
    def time_processor(self):
        return ProcessTime

    def __repr__(self):
        """
        打印当前 entity 的 json 格式 -> {"id": 1, "name": "test", ...}
        """
        obj = {}
        for field in inspect(self).attrs.keys():
            if isinstance(getattr(self, field), BaseEntity):
                entity = getattr(self, field)
                obj[field] = str(entity.module) + str(entity.primary_keys)
                continue
            if isinstance(getattr(self, field), List):
                entity_list = []
                for entity in getattr(self, field):
                    if isinstance(entity, BaseEntity):
                        entity_list.append(str(entity.module) + str(entity.primary_keys))
                        continue
                    else:
                        entity_list.append(entity)
                obj[field] = entity_list
                continue
            for field_type in self.__json_serializable_obj:
                if isinstance(getattr(self, field), field_type):
                    obj[field] = str(getattr(self, field))
                    break
                obj[field] = getattr(self, field)
        return ProcessJson.obj_to_json(obj, indent=4)

    def __del__(self):
        self.session.close()
