from typing import Optional

from src.core.exceptions.utils import ErrorCode
from src.core.exceptions.base_exception import BaseDomainException

class EntityNotFoundException(BaseDomainException):

    def __init__(self, entity_name: Optional[str] = None, message: Optional[str] = None, **kwargs):
        if not message:
            message = f"{entity_name} not found." if entity_name else "Entity not found."
        
        super().__init__(
            message=message,
            error_code=ErrorCode.ENTITY_NOT_FOUND,
            **kwargs            
        )

__all__ = ["EntityNotFoundException"]