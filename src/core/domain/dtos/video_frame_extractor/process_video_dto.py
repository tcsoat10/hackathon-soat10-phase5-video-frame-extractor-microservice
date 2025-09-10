from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Dict, Any

class ProcessVideoDTO(BaseModel):
    """DTO para os dados recebidos na task Celery."""
    job_ref: str = Field(..., description="Referência única do job.")
    client_identification: str = Field(..., description="Identificação do cliente.")
    bucket: str = Field(..., description="Nome do bucket de armazenamento.")
    video_path: str = Field(..., alias="videos_prefix", description="Caminho/prefixo do vídeo no bucket.")
    frames_path: str = Field(..., alias="frames_prefix", description="Caminho/prefixo para salvar os frames.")
    notify_url: Optional[HttpUrl] = Field(None, description="URL para notificação de callback.")
    config: Optional[Dict[str, Any]] = Field({}, description="Configurações adicionais.")

    class Config:
        populate_by_name = True

__all__ = ["ProcessVideoDTO"]
