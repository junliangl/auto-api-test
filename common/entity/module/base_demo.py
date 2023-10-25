from abc import abstractmethod

from sqlalchemy.orm import declarative_base

from common.utils.config import config
from common.entity.base_entity import BaseEntity

BaseDemoMeta = declarative_base()


class BaseDemoEntity(BaseDemoMeta, BaseEntity):

    __abstract__ = True

    @property
    def db_name(self):
        return config.demo_db_name

    @abstractmethod
    def init(self):
        pass
