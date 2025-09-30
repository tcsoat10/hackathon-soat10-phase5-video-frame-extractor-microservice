from pydantic import BaseModel, Field, ConfigDict, field_validator
from fastapi import UploadFile


class RegisterVideoDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    video_file: UploadFile = Field(..., description="Arquivo de vídeo para processamento")
    client_identification: str = Field(..., description="Identificação do cliente/usuário")
    notify_url: str = Field(None, description="URL de callback para notificação")

    @field_validator('notify_url')
    @classmethod
    def validate_notify_url(cls, value):
        if value is not None and not value.startswith(('http://', 'https://')):
            raise ValueError('notify_url must be a valid URL starting with http:// or https://')
        return value

    @field_validator('video_file')
    @classmethod
    def validate_client_identification(cls, value: UploadFile):
        if value.size > 210 * 1024 * 1024:  # 210MB
            raise ValueError('Video file size exceeds the maximum limit of 200MB')
        
        return value

__all__ = ["RegisterVideoDTO"]
