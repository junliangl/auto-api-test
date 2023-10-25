from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from common.entity.support.type.bool.bool import BoolType
from common.entity.support.type.enum.name import EnumNameType

from common.entity.module.base_demo import BaseDemoEntity


class User(BaseDemoEntity):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    dob = Column(DateTime, nullable=False)

    def init(self):
        self.name = self.math_processor.random_lower_str(5)
        self.dob = self.time_processor.current_datetime()
