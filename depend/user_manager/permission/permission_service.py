from abc import ABCMeta, abstractmethod


class PermissionService(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def user_role(*args, **kwargs):
        pass

    @staticmethod
    @abstractmethod
    def permission(*args, **kwargs):
        pass
