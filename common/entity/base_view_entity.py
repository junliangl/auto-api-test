from typing import Iterable
from abc import abstractmethod

from common.exception.no_result_error import NoResultError
from common.entity.base_entity import BaseEntity


class BaseViewEntity(BaseEntity):
    """
    视图表的基类
    """

    @property
    @abstractmethod
    def db_name(self):
        pass

    def delete_by_id(self):
        raise NoResultError(f"{self.table.name} is a view, can't delete")

    def delete_by_ids(self, ids: Iterable):
        raise NoResultError(f"{self.table.name} is a view, can't delete")

    def delete_all(self, entities=None):
        raise NoResultError(f"{self.table.name} is a view, can't delete")

    def delete_all_by_fields(self, **fields):
        raise NoResultError(f"{self.table.name} is a view, can't delete")

    def delete_all_in_fields(self, **fields: dict[str: Iterable]):
        raise NoResultError(f"{self.table.name} is a view, can't delete")

    def delete_any_in_fields(self, **fields: dict[str: Iterable]):
        raise NoResultError(f"{self.table.name} is a view, can't delete")

    def save(self):
        raise NoResultError(f"{self.table.name} is a view, can't save")

    def save_all(self, entities):
        raise NoResultError(f"{self.table.name} is a view, can't save")

    def update(self):
        raise NoResultError(f"{self.table.name} is a view, can't update")

    def init(self):
        raise NoResultError(f"{self.table.name} is a view, can't init")

    def refresh(self, auto_commit=True):
        raise NoResultError(f"{self.table.name} is a view, can't refresh")
