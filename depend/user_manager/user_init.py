from functools import wraps

from common.exception.param_error import ParamsError
from common.entity.module.profile import *
from .user_id import UserId


class UserInit:

    @staticmethod
    def customized_user(user_id=None):
        if user_id is None:
            user_id = next(UserId.customized_user_id)

        def wrapper(test_case):
            @wraps(test_case)
            def insert_user(*args, **kwargs):
                profile = Profile()
                client_profile = ClientProfile()
                user_login = UserLogin()
                profile.init()
                client_profile.init()
                user_login.init()
                user_login.id = user_id
                profile.id = user_login.id
                profile.email = user_login.email
                profile.tenant_id = user_login.tenant_id
                profile.client_profile = client_profile
                profile.user_login = user_login
                profile.save()
                kwargs["current_customized_user"] = user_login
                try:
                    test_case(*args, **kwargs)
                finally:
                    profile.client_profile.delete_by_id()
                    profile.delete_by_id()

            return insert_user

        return wrapper

    @staticmethod
    def customized_users(user_count: int):
        if user_count < 2:
            raise ParamsError(f"{user_count} must be >= 2!")
        def wrapper(test_case):
            @wraps(test_case)
            def insert_user(*args, **kwargs):
                new_profiles = []
                new_client_profiles = []
                for user_id in range(user_count):
                    new_profile = Profile()
                    new_client_profile = ClientProfile()
                    new_user_login = UserLogin()
                    new_profile.init()
                    new_client_profile.init()
                    new_user_login.init()
                    new_user_login.id = next(UserId.customized_user_id)
                    new_profile.id = new_user_login.id
                    new_profile.email = new_user_login.email
                    new_profile.tenant_id = new_user_login.tenant_id
                    new_profile.client_profile = new_client_profile
                    new_profile.user_login = new_user_login
                    new_profiles.append(new_profile)
                    new_client_profiles.append(new_profile.client_profile)
                profile = Profile()
                profile.save_all(new_profiles)
                kwargs["current_customized_users"] = [new_profile.user_login for new_profile in new_profiles]
                try:
                    test_case(*args, **kwargs)
                finally:
                    client_profile = ClientProfile()
                    client_profile.delete_all(new_client_profiles)
                    profile.delete_all(new_client_profiles)

            return insert_user

        return wrapper

    @staticmethod
    def customized_users_by_user_ids(*user_ids):
        def wrapper(test_case):
            @wraps(test_case)
            def insert_user(*args, **kwargs):
                new_profiles = []
                new_client_profiles = []
                for user_id in user_ids:
                    new_profile = Profile()
                    new_client_profile = ClientProfile()
                    new_user_login = UserLogin()
                    new_profile.init()
                    new_client_profile.init()
                    new_user_login.init()
                    new_user_login.id = user_id
                    new_profile.id = new_user_login.id
                    new_profile.email = new_user_login.email
                    new_profile.tenant_id = new_user_login.tenant_id
                    new_profile.client_profile = new_client_profile
                    new_profile.user_login = new_user_login
                    new_profiles.append(new_profile)
                    new_client_profiles.append(new_profile.client_profile)
                profile = Profile()
                profile.save_all(new_profiles)
                kwargs["current_customized_users"] = [new_profile.user_login for new_profile in new_profiles]
                try:
                    test_case(*args, **kwargs)
                finally:
                    client_profile = ClientProfile()
                    client_profile.delete_all(new_client_profiles)
                    profile.delete_all(new_client_profiles)

            return insert_user

        return wrapper
