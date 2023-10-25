class ParamsError(ValueError):
    """
    参数异常
    """

    def __init__(self, error_param):
        self.error_param = error_param

    def __str__(self):
        return f"the param is not supported, please check the param -> {self.error_param} ."
