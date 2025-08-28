from typing import Optional

from src.core.exceptions.utils import ErrorCode
from src.core.exceptions.base_exception import BaseDomainException


class BadRequestException(BaseDomainException):
    def __init__(self, message: Optional[str] = "Bad Request", **kwargs):
        super().__init__(
            message=message,
            error_code=ErrorCode.BAD_REQUEST,
            **kwargs
        )

__all__ = ["BadRequestException"]
    