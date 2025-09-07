from src.core.application.use_cases.register_video_use_case import RegisterVideoUseCase
from src.core.domain.dtos.video_frame_extractor.register_video_dto import RegisterVideoDTO
from src.core.domain.dtos.video_frame_extractor.video_job_dto import VideoJobDTO
from src.core.ports.cloud.object_storage_gateway import ObjectStorageGateway
from src.core.ports.repositories.i_video_job_repository import IVideoJobRepository
from src.core.ports.tasks.i_task_queue_gateway import ITaskQueueGateway
from src.presentation.api.v1.presenters.dto_presenter import DTOPresenter

class VideoController:
    def __init__(
        self,
        video_job_repository: IVideoJobRepository,
        storage_gateway: ObjectStorageGateway,
        task_gateway: ITaskQueueGateway
    ):
        self._video_job_repository = video_job_repository
        self._storage_gateway = storage_gateway
        self._task_gateway = task_gateway

    async def register_video(self, dto: RegisterVideoDTO) -> VideoJobDTO:
        register_video_use_case: RegisterVideoUseCase = RegisterVideoUseCase.build(
            video_job_repository=self._video_job_repository,
            storage_gateway=self._storage_gateway,
            task_gateway=self._task_gateway
        )
        video_job_entity = await register_video_use_case.execute(dto)
        return DTOPresenter.transform(video_job_entity, VideoJobDTO)

__all__ = ["VideoController"]
