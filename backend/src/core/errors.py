from src.models.message import ErrorMessage

class BackendError(Exception):
    def __init__(self, message: ErrorMessage):
        super().__init__()
        self.args = (message,)

class AccessError(BackendError):
    def __init__(self, message: str = "Access Denied"):
        super().__init__(ErrorMessage(text=message, code=403))

class NotFoundError(BackendError):
    def __init__(self, message: str = "Not Found"):
        super().__init__(ErrorMessage(text=message, code=404))

class DataBaseError(BackendError):
    def __init__(self, message: str = "Data base internal error"):
        super().__init__(ErrorMessage(text=message, code=500))

class AlreadyExistError(BackendError):
    def __init__(self, message: str = "Already exist"):
        super().__init__(ErrorMessage(text=message, code=409))
