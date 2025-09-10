from abc import ABC, abstractmethod
from typing import Optional
from src.core.domain.entities.video_job import VideoJob

class IVideoJobRepository(ABC):
    @abstractmethod
    def save(self, video_job: VideoJob) -> VideoJob:
        pass

    @abstractmethod
    def find_by_job_ref(self, job_ref: str) -> Optional[VideoJob]:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[VideoJob]:
        pass

__all__ = ["IVideoJobRepository"]
