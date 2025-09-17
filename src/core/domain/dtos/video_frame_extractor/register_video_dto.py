from pydantic import BaseModel, Field, ConfigDict
from fastapi import UploadFile
from typing import Optional

from src.core.domain.dtos.video_frame_extractor.register_video_config_dto import RegisterVideoConfigDTO

class RegisterVideoDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    video_file: UploadFile = Field(..., description="Arquivo de vídeo para processamento")
    client_identification: str = Field(..., description="Identificação do cliente/usuário")
    notify_url: Optional[str] = Field(None, description="URL de callback para notificação")
    # config: Optional[RegisterVideoConfigDTO] = Field(None, description="Configurações adicionais do job")
        
__all__ = ["RegisterVideoDTO"]
