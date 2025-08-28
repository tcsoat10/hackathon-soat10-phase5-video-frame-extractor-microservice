import os
from typing import Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import Match

class ApiKeyMiddleware(BaseHTTPMiddleware):
    """Middleware para validar a chave de API (x-api-key) nas requisições."""

    EXCLUDED_PATHS = [
        "/docs",
        "/redoc",
        "/openapi.json",
        "/favicon.ico",
        "/docs/oauth2-redirect",
        "/api/v1/health",
    ]

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if request.url.path in self.EXCLUDED_PATHS:
            return await call_next(request)

        for route in request.app.routes:
            match, _ = route.matches(request.scope)
            if match == Match.FULL:
                if hasattr(route.endpoint, 'bypass_auth'):
                    return await call_next(request)
                break

        video_frame_extractor_microservice_x_api_key = os.getenv("VIDEO_FRAME_EXTRACTOR_MICROSERVICE_X_API_KEY")
        api_key = request.headers.get("x-api-key")

        if not video_frame_extractor_microservice_x_api_key:
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error: API Key not configured on server."}
            )

        if not api_key or api_key != video_frame_extractor_microservice_x_api_key:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or missing API Key"}
            )

        return await call_next(request)
