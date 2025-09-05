from mongoengine import StringField, DictField
from src.core.shared.identity_map import IdentityMap
from src.infrastructure.repositories.mongoengine.models.base_model import BaseModel
from src.core.constants.video_job_status import VideoJobStatus
from src.core.domain.entities.video_job import VideoJob


class VideoJobModel(BaseModel):
    """Modelo MongoEngine para VideoJob."""
    meta = {'collection': 'video_jobs', 'indexes': ['job_ref']}

    job_ref = StringField(required=True, unique=True)
    client_identification = StringField(required=True)
    # status = EnumField(VideoJobStatus, default=VideoJobStatus.PENDING)
    status = StringField(required=True, choices=VideoJobStatus.method_list())
    bucket = StringField(required=True)
    video_path = StringField(required=True)
    frames_path = StringField(required=True)
    notify_url = StringField()
    config = DictField()
    error_message = StringField()
    
    @classmethod
    def from_entity(cls, video_job: VideoJob) -> "VideoJobModel":
        return cls(
            id=video_job.id,
            job_ref=video_job.job_ref,
            client_identification=video_job.client_identification,
            status=video_job.status,
            bucket=video_job.bucket,
            video_path=video_job.video_path,
            frames_path=video_job.frames_path,
            notify_url=video_job.notify_url,
            config=video_job.config,
            error_message=video_job.error_message
        )
    
    def to_entity(self) -> VideoJob:
        identity_map: IdentityMap = IdentityMap.get_instance()
        existing_entity: VideoJob = identity_map.get(VideoJob, self.id)
        if existing_entity:
            return existing_entity
        
        video_job = VideoJob(
            id=self.id,
            job_ref=self.job_ref,
            client_identification=self.client_identification,
            status=self.status,
            bucket=self.bucket,
            video_path=self.video_path,
            frames_path=self.frames_path,
            notify_url=self.notify_url,
            config=self.config,
            error_message=self.error_message
        )
        
        identity_map.add(video_job)
        return video_job
        

__all__ = ["VideoJobModel"]