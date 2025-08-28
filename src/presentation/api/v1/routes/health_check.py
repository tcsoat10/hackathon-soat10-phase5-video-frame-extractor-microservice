from fastapi import APIRouter, status
from pydantic import BaseModel, ConfigDict

router = APIRouter()

class HealthResponse(BaseModel):
    status: str

    model_config = ConfigDict(json_schema_extra={"example": {"status": "ok"}})

@router.get(
    "/health",
    response_model=HealthResponse,
    response_description="Status do serviço",
    status_code=status.HTTP_200_OK,
)
async def health_check():
    return {"status": "ok"}
