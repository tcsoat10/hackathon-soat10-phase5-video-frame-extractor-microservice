
from src.core.exceptions.utils import ErrorCode
from src.core.exceptions.base_exception import BaseDomainException

class EntityDuplicatedException(BaseDomainException):

    def __init__(self, entity_name: str, **kwargs):
        super().__init__(
            message=f"{entity_name} already exists.",
            error_code=ErrorCode.DUPLICATED_ENTITY,
            **kwargs
        )

__all__ = ["EntityDuplicatedException"]
