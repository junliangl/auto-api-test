from typing import List

from pytest import fixture

from common.utils.http_service import HttpService
from common.utils.db.sqlalchemy.sqlalchemy_session import SqlalchemySession
from common.entity.module.demo.user import User
from depend.user_manager import normal_user_id


@fixture(scope="session")
def http_request():
    http_request = HttpService()
    yield http_request
    http_request.close()


@fixture(scope="function")
def header() -> dict:
    yield {}


@fixture(scope="function")
def current_user():
    yield


@fixture(scope="function")
def current_customized_user() -> User:
    yield


@fixture(scope="function")
def current_customized_users() -> List[User]:
    yield


@fixture(scope="session")
def demo_db() -> SqlalchemySession:
    return SqlalchemySession.demo_db()
