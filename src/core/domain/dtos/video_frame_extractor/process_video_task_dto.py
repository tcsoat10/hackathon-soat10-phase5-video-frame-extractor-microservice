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
{
    'job_ref': 'aaa-e5c6fb3f-2349-49fc-8012-1330405d4231',
    'client_identification': 'aaa',
    'bucket': 'default-bucket',
    'video_path': 'default-path-video',
    'frames_path': 'default-path-frames',
    'notify_url': 'bbb', 'config': {}
}