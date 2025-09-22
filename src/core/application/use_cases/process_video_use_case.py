import os
import tempfile
from typing import List

from src.core.domain.dtos.video_frame_extractor.process_video_task_dto import ProcessVideoTaskDTO
from src.core.domain.entities.video_job import VideoJob
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.gateways.callbacks.i_notification_gateway import INotificationGateway
from src.core.ports.repositories.i_video_job_repository import IVideoJobRepository
from src.core.ports.cloud.object_storage_gateway import ObjectStorageGateway
from src.infrastructure.video.ffmpeg_wrapper import FFmpegWrapper

class ProcessVideoUseCase:
    def __init__(
        self,
        video_job_repository: IVideoJobRepository,
        storage_gateway: ObjectStorageGateway,
        video_processor: FFmpegWrapper,
        notification_gateway: INotificationGateway,
    ):
        self._video_job_repository = video_job_repository
        self._storage_gateway = storage_gateway
        self._video_processor = video_processor
        self._notification_gateway = notification_gateway
        
    def _send_notification(self, video_job: VideoJob):
        notification = video_job.build_notification()
        self._notification_gateway.send_notification(
            notify_url=video_job.notify_url,
            notification_dto=notification
        )

    @classmethod
    def build(
        cls,
        video_job_repository: IVideoJobRepository,
        storage_gateway: ObjectStorageGateway,
        video_processor: FFmpegWrapper,
        notification_gateway: INotificationGateway,
    ) -> "ProcessVideoUseCase":
        return cls(video_job_repository, storage_gateway, video_processor, notification_gateway)

    def execute(self, dto: ProcessVideoTaskDTO):
        video_job = self._video_job_repository.find_by_job_ref(dto.job_ref)
        if not video_job:
            raise EntityNotFoundException(message=f"VideoJob com job_ref {dto.job_ref} não encontrado.")
        
        try:
            video_job.start_processing()
            self._video_job_repository.save(video_job)
            
            video_bytes = self._storage_gateway.download_object(
                bucket=video_job.bucket,
                key=f"{video_job.video_path}/{video_job.client_identification}/{video_job.job_ref}"
            )

            with tempfile.TemporaryDirectory() as temp_dir:
                temp_video_path = os.path.join(temp_dir, 'input_video')
                with open(temp_video_path, 'wb') as f:
                    f.write(video_bytes)

                frame_paths = self._video_processor.extract_frames(temp_video_path, temp_dir)
                self._upload_frames_in_bulk(frame_paths, video_job)

            video_job.complete()
            self._video_job_repository.save(video_job)
            
            self._send_notification(video_job)

            return {
                "job_ref": video_job.job_ref,
                "client_identification": video_job.client_identification,
                "bucket": video_job.bucket,
                "frames_path": f"{video_job.frames_path}/{video_job.client_identification}/{video_job.job_ref}",
                "notify_url": video_job.notify_url,
            }

        except Exception as e:
            import traceback
            traceback.print_exc()
            error_message = f"Failed to process video: {e}"
            
            if video_job:
                video_job.fail(error_message)
                self._video_job_repository.save(video_job)
                self._send_notification(video_job, detail=error_message)

            raise

    def _upload_frames_in_bulk(self, frame_paths: List[str], video_job: VideoJob):
        items_to_upload = []
        for frame_path in frame_paths:
            with open(frame_path, 'rb') as f:
                content = f.read()

            frame_filename = os.path.basename(frame_path)
            key_suffix = f"{frame_filename}"
            
            items_to_upload.append((content, key_suffix))

        self._storage_gateway.upload_objects_bulk(
            items=items_to_upload,
            bucket=video_job.bucket,
            prefix=f"{video_job.frames_path}/{video_job.client_identification}/{video_job.job_ref}",
            content_type='image/png'
        )
