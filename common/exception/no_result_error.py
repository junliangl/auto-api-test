class NoResultError(NotImplementedError):
    """
    访问的属性暂时没有合适的结果
    """

    def __init__(self, error_message):
        self.error_message = error_message

    def __str__(self):
        return f"No Suitable Result! Cause: {self.error_message}"
