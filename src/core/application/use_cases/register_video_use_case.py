from src.config.settings import STORAGE_BUCKET, STORAGE_FRAMES_PATH, STORAGE_VIDEO_PATH
from src.core.constants.video_job_status import VideoJobStatus
from src.core.domain.dtos.video_frame_extractor.register_video_dto import RegisterVideoDTO
from src.core.domain.entities.video_job import VideoJob
from src.core.domain.entities.storage_item import StorageItem
from src.core.ports.repositories.i_video_job_repository import IVideoJobRepository
from src.core.ports.cloud.object_storage_gateway import ObjectStorageGateway
from src.core.ports.tasks.i_task_queue_gateway import ITaskQueueGateway

class RegisterVideoUseCase:
    def __init__(
        self,
        video_job_repository: IVideoJobRepository,
        storage_gateway: ObjectStorageGateway,
        task_gateway: ITaskQueueGateway,
    ):
        self._video_job_repository = video_job_repository
        self._storage_gateway = storage_gateway
        self._task_gateway = task_gateway
        
    @classmethod
    def build(
        cls,
        video_job_repository: IVideoJobRepository,
        storage_gateway: ObjectStorageGateway,
        task_gateway: ITaskQueueGateway,
    ) -> "RegisterVideoUseCase":
        return cls(video_job_repository, storage_gateway, task_gateway)

    async def execute(self, dto: RegisterVideoDTO) -> VideoJob:
        video_job = VideoJob(
            job_ref='',
            client_identification=dto.client_identification,
            status=VideoJobStatus.PENDING.status,
            bucket=STORAGE_BUCKET,
            video_path=STORAGE_VIDEO_PATH,
            frames_path=STORAGE_FRAMES_PATH,
            notify_url=dto.notify_url,
            config={},
        )

        video_job.id=None
        saved_job = self._video_job_repository.save(video_job)
        video_content = await dto.video_file.read()
        storage_item = StorageItem(
            bucket=STORAGE_BUCKET,
            key=f"{STORAGE_VIDEO_PATH}/{saved_job.job_ref}",
            content=video_content,
            content_type=dto.video_file.content_type
        )
        self._storage_gateway.upload_object(storage_item)

        task_data = {
            "job_ref": saved_job.job_ref,
            "client_identification": saved_job.client_identification,
            "bucket": saved_job.bucket,
            "video_path": saved_job.video_path,
            "frames_path": saved_job.frames_path,
            "notify_url": saved_job.notify_url,
            "config": saved_job.config,
        }
        self._task_gateway.enqueue_video_processing_task(task_data)

        return saved_job

__all__ = ["RegisterVideoUseCase"]
