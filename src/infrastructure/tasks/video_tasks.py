from typing import Dict, Any
from dependency_injector.wiring import inject, Provide
from src.config.celery_app import celery_app
from src.core.application.use_cases.send_video_to_zipper_use_case import SendVideoToZipperUseCase
from src.core.containers import Container
from src.core.ports.gateways.zipper.i_zipper_gateway import IZipperGateway
from src.core.ports.repositories.i_video_job_repository import IVideoJobRepository
from src.core.ports.cloud.object_storage_gateway import ObjectStorageGateway
from src.infrastructure.video.ffmpeg_wrapper import FFmpegWrapper
from src.core.domain.dtos.video_frame_extractor.process_video_task_dto import ProcessVideoTaskDTO
from src.core.application.use_cases.process_video_use_case import ProcessVideoUseCase


@celery_app.task(
    name='src.infrastructure.tasks.video_tasks.extract_frames_task',
    bind=True,
    acks_late=True,
)
@inject
def extract_frames_task(
    self,
    task_data: Dict[str, Any],
    video_job_repository: IVideoJobRepository = Provide[Container.video_job_repository],
    storage_gateway: ObjectStorageGateway = Provide[Container.object_storage_gateway],
    ffmpeg_wrapper: FFmpegWrapper = Provide[Container.ffmpeg_wrapper],
    zipper_gateway: IZipperGateway = Provide[Container.zipper_gateway],
    notification_gateway = Provide[Container.notification_gateway],
):
    try:
        print(f"Iniciando task {self.request.id} com dados: {task_data}")
        dto = ProcessVideoTaskDTO(**task_data)
        
        process_video_use_case = ProcessVideoUseCase.build(
            video_job_repository=video_job_repository,
            storage_gateway=storage_gateway,
            video_processor=ffmpeg_wrapper,
            notification_gateway=notification_gateway
        )
        video_process_result = process_video_use_case.execute(dto)
        
        send_video_to_zipper_use_case = SendVideoToZipperUseCase.build(
            zipper_gateway=zipper_gateway
        )
        send_video_to_zipper_use_case.execute(video_process_result)

        print(f"Task {self.request.id} concluída com sucesso.")
        return {'status': 'success', 'job_ref': dto.job_ref}
    except Exception as e:
        import traceback
        traceback.print_exc()
        
        print(f"Erro na task {self.request.id}: {e}")

        raise self.retry(exc=e, countdown=60)

