from datetime import datetime
from typing import Dict, Optional, Any

from src.core.domain.dtos.callbacks.notification_dto import NotificationDTO
from src.core.domain.entities.base_entity import BaseEntity
from src.core.constants.video_job_status import VideoJobStatus

class VideoJob(BaseEntity):
    """Entidade que representa um trabalho de processamento de vídeo."""

    def __init__(
        self,
        job_ref: str,
        client_identification: str,
        status: str,
        bucket: str,
        video_path: str,
        frames_path: str,
        notify_url: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        inactivated_at: Optional[datetime] = None
    ):
        super().__init__(
            id=id,
            created_at=created_at or datetime.now(), 
            updated_at=updated_at or datetime.now(), 
            inactivated_at=inactivated_at
        )
        self.job_ref = job_ref
        self.client_identification = client_identification
        self.status = status
        self.bucket = bucket
        self.video_path = video_path
        self.frames_path = frames_path
        self.notify_url = notify_url
        self.config = config or {}
        self.error_message = error_message

    def enqueue(self):
        if self.status != VideoJobStatus.PENDING.status:
            print(f"Warning: Job {self.job_ref} não está em estado PENDING.")
            return
        self.status = VideoJobStatus.QUEUED.status
        self.updated_at = datetime.now()
    
    def start_processing(self):
        if self.status != VideoJobStatus.QUEUED.status:
            print(f"Warning: Job {self.job_ref} já foi iniciado.")
            return
        self.status = VideoJobStatus.PROCESSING.status
        self.updated_at = datetime.now()

    def complete(self):
        self.status = VideoJobStatus.COMPLETED.status
        self.error_message = None
        self.updated_at = datetime.now()

    def fail(self, reason: str):
        self.status = VideoJobStatus.ERROR.status
        self.error_message = reason
        self.updated_at = datetime.now()
        self.inactivated_at = datetime.now()
        
    def build_notification(self, detail: str = None):
        return NotificationDTO(
            job_ref=self.job_ref,
            status=self.status,
            timestamp=datetime.now().isoformat(),
            detail=detail,
            service="frame_extractor"
        )

__all__ = ["VideoJob"]
