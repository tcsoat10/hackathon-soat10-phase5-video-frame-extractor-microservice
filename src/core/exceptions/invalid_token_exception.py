
from src.core.exceptions.base_exception import BaseDomainException
from src.core.exceptions.utils import ErrorCode

class InvalidTokenException(BaseDomainException):
    def __init__(self, **kwargs):
        message = kwargs.pop("message")
        super().__init__(
            error_code=ErrorCode.INVALID_TOKEN,
            message= message or "Invalid token payload",
            **kwargs,
        )
