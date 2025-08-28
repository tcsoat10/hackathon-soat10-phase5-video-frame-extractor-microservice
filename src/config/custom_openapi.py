from typing import Any, Dict
from fastapi import FastAPI


def custom_openapi(app: FastAPI) -> Dict[str, Any]:
    """
    Configuração personalizada do OpenAPI com suporte para autenticação por API Key
    """
    if app.openapi_schema:
        return app.openapi_schema
    
    from fastapi.openapi.utils import get_openapi
    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "apiKey": {
            "type": "apiKey",
            "in": "header",
            "name": "x-api-key",
            "description": "API Key necessária para acessar os endpoints protegidos"
        }
    }
    
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if not path.startswith("/api/v1/health"):
                openapi_schema["paths"][path][method]["security"] = [{"apiKey": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema
