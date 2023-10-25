from abc import abstractmethod

from sqlalchemy.types import TypeDecorator


class BaseType(TypeDecorator):

    @abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @abstractmethod
    def process_bind_param(self, value, dialect):
        pass

    @abstractmethod
    def process_result_value(self, value, dialect):
        pass

    def process_literal_param(self, value, dialect):
        return super().process_literal_param(value, dialect)

    @property
    def python_type(self):
        return super().python_type
