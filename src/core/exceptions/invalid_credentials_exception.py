
from src.core.exceptions.utils import ErrorCode
from src.core.exceptions.base_exception import BaseDomainException

class InvalidCredentialsException(BaseDomainException):

    def __init__(self, **kwargs):
        super().__init__(
            message="Usuário ou senha inválidos.",
            error_code=ErrorCode.INVALID_CREDENTIALS,
            **kwargs
        )

__all__ = ["InvalidCredentialsException"]
