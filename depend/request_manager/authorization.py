from enum import Enum
from functools import wraps

from common.utils.http_service import HttpService
from common.utils.decorator import Decorator
from common.entity.module.demo.user import User


@Decorator.const_single
class Authorization:

    __default_request_type = {"content-type": "application/json"}

    class HeaderType(Enum):

        AUTHORIZATION = "authorization"
        DEBUG_USER = "debug-user"
        API_TOKEN = "api-token"
        KEY = "key"
        BEARER_TOKEN = "Authorization"
        GAIA = "X-account-env"

    def __set_authorization_header_(self, current_user):
        header = {"authorization": f"{current_user.id}"}
        header.update(self.__default_request_type)
        return header

    def __set_debug_user_header_(self, current_user):
        header = {"debug-user": f"{current_user.id}"}
        header.update(self.__default_request_type)
        return header

    def __set_api_token_user_header_(self, current_user):
        current_user.api_token = current_user.math_processor.random_lower_str(5)
        current_user.update()
        header = {"api-token": current_user.api_token}
        header.update(self.__default_request_type)
        return header

    def __set_key_header_(self, current_user):
        raise NotImplementedError

    def __set_bearer_token_header_(self, current_user):
        raise NotImplementedError

    def __set_gaia_header_(self, current_user):
        raise NotImplementedError

    def header(self, header_type: HeaderType, user_type=None):

        def wrapper(test_case):
            @wraps(test_case)
            def set_header(*args, **kwargs):
                if user_type is None:
                    current_user: User = kwargs.get("current_user")
                else:
                    current_user = kwargs.get(user_type)
                if header_type is None or not isinstance(header_type, self.HeaderType):
                    pass
                elif header_type is self.HeaderType.AUTHORIZATION:
                    kwargs["header"] = self.__set_authorization_header_(current_user)
                elif header_type is self.HeaderType.DEBUG_USER:
                    kwargs["header"] = self.__set_debug_user_header_(current_user)
                elif header_type is self.HeaderType.API_TOKEN:
                    kwargs["header"] = self.__set_api_token_user_header_(current_user)
                elif header_type is self.HeaderType.KEY:
                    kwargs["header"] = self.__set_key_header_(current_user)
                elif header_type is self.HeaderType.BEARER_TOKEN:
                    kwargs["header"] = self.__set_bearer_token_header_(current_user)
                elif header_type is self.HeaderType.GAIA:
                    kwargs["header"] = self.__set_gaia_header_(current_user)
                return test_case(*args, **kwargs)
            return set_header
        return wrapper


authorization = Authorization()
