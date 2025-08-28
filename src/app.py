from src.core.containers import Container
from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.config.database import connect_db, disconnect_db
from src.config.custom_openapi import custom_openapi
from src.presentation.api.v1.middleware.api_key_middleware import ApiKeyMiddleware
from src.presentation.api.v1.middleware.custom_error_middleware import CustomErrorMiddleware
from src.presentation.api.v1.middleware.identity_map_middleware import IdentityMapMiddleware
from src.presentation.api.v1.routes.health_check import router as health_check_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_db()
    yield
    disconnect_db()

app = FastAPI(
    title="Video Frame Extractor Microservice - FIAP",
    lifespan=lifespan,
    description="Microservice responsible for extracting frames from videos.",
    version="0.1.0",
    swagger_ui_init_oauth={
        "appName": "Tech Challenger SOAT10 - FIAP - Swagger UI",
        "clientId": "docs",
        "clientSecret": "docs",
        "useBasicAuthenticationWithAccessCodeGrant": True,
    },
    swagger_ui_oauth2_redirect_url="/docs/oauth2-redirect",
    swagger_ui_parameters={
        "persistAuthorization": True,
    },
)

container = Container()
app.container = container

app.openapi = lambda: custom_openapi(app)

app.add_middleware(ApiKeyMiddleware)
app.add_middleware(CustomErrorMiddleware)
app.add_middleware(IdentityMapMiddleware)


app.include_router(health_check_router, prefix="/api/v1")
