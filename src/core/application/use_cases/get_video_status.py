from src.core.domain.dtos.video_frame_extractor.video_job_dto import VideoJobDTO
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.repositories.i_video_job_repository import IVideoJobRepository

class GetVideoStatusUseCase:
    def __init__(self, video_job_repository: IVideoJobRepository):
        self._video_job_repository = video_job_repository

    @classmethod
    def build(cls, video_job_repository: IVideoJobRepository) -> "GetVideoStatusUseCase":
        return cls(video_job_repository)

    async def execute(self, job_ref: str) -> VideoJobDTO:
        video_job = self._video_job_repository.find_by_job_ref(job_ref)
        if not video_job:
            raise EntityNotFoundException(message=f"VideoJob com job_ref {job_ref} não encontrado.")
        return VideoJobDTO.from_entity(video_job)

__all__ = ["GetVideoStatusUseCase"]
