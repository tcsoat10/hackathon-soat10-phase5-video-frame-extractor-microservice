from typing import Optional
from uuid import uuid4
from src.core.domain.entities.video_job import VideoJob
from src.core.ports.repositories.i_video_job_repository import IVideoJobRepository
from src.infrastructure.repositories.mongoengine.models.video_job_model import VideoJobModel

class MongoVideoJobRepository(IVideoJobRepository):

    def save(self, video_job: VideoJob) -> VideoJob:
        """Salva ou atualiza um VideoJob."""
        if not video_job.id:
            video_job.job_ref = f"{video_job.client_identification}-{uuid4()}"
            model = VideoJobModel.from_entity(video_job)
        else:
            model = VideoJobModel.objects(id=video_job.id).first()
            if not model:
                raise ValueError(f"VideoJob com ID {video_job.id} não encontrado para atualização.")

            model.status = video_job.status
            model.error_message = video_job.error_message
            model.updated_at = video_job.updated_at

        model.save()

        return model.to_entity()

    def find_by_job_ref(self, job_ref: str) -> Optional[VideoJob]:
        model: VideoJobModel = VideoJobModel.objects(job_ref=job_ref).first()
        print(model)
        return model.to_entity() if model else None
    
    def get_by_id(self, id: str) -> Optional[VideoJob]:
        """Busca um VideoJob pelo id."""
        model: VideoJobModel = VideoJobModel.objects(id=id).first()
        return model.to_entity() if model else None

__all__ = ["MongoVideoJobRepository"]
