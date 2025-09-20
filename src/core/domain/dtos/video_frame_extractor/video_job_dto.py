from pydantic import BaseModel
from datetime import datetime

from src.core.domain.entities.video_job import VideoJob

class VideoJobDTO(BaseModel):
    id: str
    client_identification: str
    job_ref: str
    status: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: VideoJob) -> "VideoJobDTO":
        return cls(
            id=str(entity.id),
            client_identification=entity.client_identification,
            job_ref=entity.job_ref,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

__all__ = ["VideoJobDTO"]
