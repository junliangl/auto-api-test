from itertools import count


class UserId:

    normal_user_id = count(start=100001, step=1)
    ib_user_id = count(start=99999, step=-1)
    customized_user_id = count(start=200001, step=1)
