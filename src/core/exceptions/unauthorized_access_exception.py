from typing import Optional
from src.core.exceptions.utils import ErrorCode
from src.core.exceptions.base_exception import BaseDomainException


class UnauthorizedAccessException(BaseDomainException):
    def __init__(self, message: Optional[str] = "Unauthorized", **kwargs):
        super().__init__(
            message=message,
            error_code=ErrorCode.UNAUTHORIZED,
            **kwargs
        )

__all__ = ["UnauthorizedAccessException"]
    