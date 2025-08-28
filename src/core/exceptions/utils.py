from enum import Enum

class ErrorCode(Enum):
    ENTITY_NOT_FOUND = ("ENTITY_NOT_FOUND", "The requested entity was not found.")
    DUPLICATED_ENTITY = ("DUPLICATED_ENTITY", "The entity already exists.")
    INVALID_CREDENTIALS = ("INVALID_CREDENTIALS", "Invalid username or password.")
    INVALID_TOKEN = ("INVALID_TOKEN", "Invalid token payload.")
    UNEXPECTED_ERROR = ("UNEXPECTED_ERROR", "An unexpected error occurred.")
    VALIDATION_ERROR = ("VALIDATION_ERROR", "Validation failed for the input.")
    FORBIDDEN = ("FORBIDDEN", "Access denied.")
    UNAUTHORIZED = ("UNAUTHORIZED", "Unauthorized.")
    BAD_REQUEST = ("BAD_REQUEST", "Bad request.")
    INTERNAL_SERVER_ERROR = ("INTERNAL_SERVER_ERROR", "Internal server error.")

    def __init__(self, value: str, description: str):
        self._value_ = value
        self.description = description

    def __str__(self):
        return self.value

__all__ = ["ErrorCode"]
