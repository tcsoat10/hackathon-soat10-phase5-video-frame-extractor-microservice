from typing import Optional

from src.core.exceptions.utils import ErrorCode
from src.core.exceptions.base_exception import BaseDomainException

class ForbiddenException(BaseDomainException):
    def __init__(self, message: Optional[str] = "Forbidden", **kwargs):
        super().__init__(
            message=message,
            error_code=ErrorCode.FORBIDDEN,
            **kwargs
        )

__all__ = ["ForbiddenException"]
