from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class ProcessVideoTaskDTO(BaseModel):
    job_ref: str = Field(..., description="Referência única para o job")
    client_identification: str = Field(..., description="Identificação do cliente/usuário")
    bucket: str = Field(..., description="Nome do bucket de armazenamento")
    video_path: str = Field(..., description="Caminho/prefixo onde o vídeo está salvo")
    frames_path: str = Field(..., description="Caminho/prefixo onde os frames serão salvos")
    notify_url: Optional[str] = Field(None, description="URL de callback para notificação")
    config: Optional[Dict[str, Any]] = Field({}, description="Configurações adicionais do job")

__all__ = ["ProcessVideoTaskDTO"]
