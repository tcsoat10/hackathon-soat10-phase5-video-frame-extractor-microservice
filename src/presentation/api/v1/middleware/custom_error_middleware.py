from fastapi import status
from fastapi.responses import JSONResponse
import logging

from src.core.exceptions.bad_request_exception import BadRequestException
from src.core.exceptions.base_exception import BaseDomainException
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.exceptions.forbidden_exception import ForbiddenException
from src.core.exceptions.invalid_credentials_exception import InvalidCredentialsException
from src.core.exceptions.invalid_token_exception import InvalidTokenException
from src.core.exceptions.unauthorized_access_exception import UnauthorizedAccessException
from src.core.exceptions.validation_exception import ValidationException

class CustomErrorMiddleware:
    def __init__(self, app):
        self.app = app
        
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        try:
            await self.app(scope, receive, send)
        except BaseDomainException as exc:
            logging.warning(f"Middleware capturou exceção: {exc}")
            response = self._create_json_response(exc)
            await response(scope, receive, send)
        except Exception as exc:
            logging.error(f"Unhandled exception: {exc}", exc_info=True)
            response = self._create_json_response(exc)
            await response(scope, receive, send)
            
    def _create_json_response(self, exc):
        status_code_map = {
            EntityNotFoundException: status.HTTP_404_NOT_FOUND,
            EntityDuplicatedException: status.HTTP_409_CONFLICT,
            ForbiddenException: status.HTTP_403_FORBIDDEN,
            UnauthorizedAccessException: status.HTTP_401_UNAUTHORIZED,
            InvalidCredentialsException: status.HTTP_401_UNAUTHORIZED,
            InvalidTokenException: status.HTTP_401_UNAUTHORIZED,
            ValidationException: status.HTTP_422_UNPROCESSABLE_ENTITY,
            BadRequestException: status.HTTP_400_BAD_REQUEST
        }
        status_code = status_code_map.get(type(exc), status.HTTP_500_INTERNAL_SERVER_ERROR)

        detail = getattr(exc, "detail", {})
        if isinstance(detail, dict):
            error_code = detail.get("code", "UNKNOWN_ERROR")
            message = detail.get("message", str(exc))
            details = detail.get("details", {})
        else:
            error_code = "UNKNOWN_ERROR"
            message = str(exc)
            details = {}

        headers = {"WWW-Authenticate": "Bearer"} if status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN] else None

        return JSONResponse(
            status_code=status_code,
            content={
                "detail": {
                    "code": error_code,
                    "message": message,
                    "details": details,
                }
            },
            headers=headers
        )
