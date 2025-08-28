import logging
from typing import Optional

from src.core.exceptions.utils import ErrorCode

class BaseDomainException(Exception):
    def __init__(self, message: str = None, error_code: Optional[ErrorCode] = None, details: Optional[dict] = None):
        logging.error(f"Error {error_code}: {message} - Details: {details}")
        self.detail = {
            "message": message or error_code.description,
            "code": str(error_code),
            "details": details
        }
        super().__init__(message)

__all__ = ["BaseDomainException"]