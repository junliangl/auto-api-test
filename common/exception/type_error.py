class TypesError(TypeError):
    """
    类型异常
    """

    def __init__(self, error_param):
        self.error_type = type(error_param)

    def __str__(self):
        return f"the type is not supported, please check the type -> {self.error_type} ."
