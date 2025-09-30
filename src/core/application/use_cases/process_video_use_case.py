import os
import tempfile
from typing import List

from src.core.domain.dtos.video_frame_extractor.process_video_task_dto import ProcessVideoTaskDTO
from src.core.domain.entities.storage_item import StorageItem
from src.core.domain.entities.video_job import VideoJob
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.gateways.callbacks.i_notification_gateway import INotificationGateway
from src.core.ports.repositories.i_video_job_repository import IVideoJobRepository
from src.core.ports.cloud.object_storage_gateway import ObjectStorageGateway
from src.core.ports.cloud.content_moderation_gateway import ContentModerationGateway
from src.infrastructure.video.ffmpeg_wrapper import FFmpegWrapper

class ProcessVideoUseCase:
    def __init__(
        self,
        video_job_repository: IVideoJobRepository,
        storage_gateway: ObjectStorageGateway,
        video_processor: FFmpegWrapper,
        notification_gateway: INotificationGateway,
        content_moderation_gateway: ContentModerationGateway,
    ):
        self._video_job_repository = video_job_repository
        self._storage_gateway = storage_gateway
        self._video_processor = video_processor
        self._notification_gateway = notification_gateway
        self._content_moderation_gateway = content_moderation_gateway
        
    def _send_notification(self, video_job: VideoJob, detail: str = None):
        notification = video_job.build_notification(detail=detail)
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
        content_moderation_gateway: ContentModerationGateway,
    ) -> "ProcessVideoUseCase":
        return cls(video_job_repository, storage_gateway, video_processor, notification_gateway, content_moderation_gateway)

    def execute(self, dto: ProcessVideoTaskDTO):
        video_job = self._video_job_repository.find_by_job_ref(dto.job_ref)
        if not video_job:
            raise EntityNotFoundException(message=f"VideoJob com job_ref {dto.job_ref} não encontrado.")
        
        try:
            video_job.start_processing()
            self._video_job_repository.save(video_job)
            
            # Moderação de conteúdo antes de processar o vídeo
            video_key = f"{video_job.video_path}/{video_job.client_identification}/{video_job.job_ref}"
            moderation_result = self._content_moderation_gateway.moderate_video_content(
                bucket=video_job.bucket,
                video_key=video_key
            )
            
            print(f"Moderação de conteúdo concluída: {moderation_result}")
            
            # Se o conteúdo não for apropriado, rejeita o vídeo
            if not moderation_result.get("is_appropriate", True):
                labels = moderation_result.get("labels", [])
                label_names = [label.get("name", "") for label in labels]
                rejection_reason = f"Conteúdo inadequado detectado: {', '.join(label_names)}"
                
                video_job.reject(rejection_reason)
                self._video_job_repository.save(video_job)
                self._send_notification(video_job, detail=rejection_reason)
                
                return {
                    "job_ref": video_job.job_ref,
                    "client_identification": video_job.client_identification,
                    "status": video_job.status,
                    "reason": rejection_reason,
                }
            
            # Se o conteúdo foi aprovado, continua com o processamento normal
            video_bytes = self._storage_gateway.download_object(
                bucket=video_job.bucket,
                key=video_key
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
        for frame_path in frame_paths:
            with open(frame_path, 'rb') as frame_file:
                self._storage_gateway.upload_file_obj(
                    StorageItem(
                        bucket=video_job.bucket,
                        key=f"{video_job.frames_path}/{video_job.client_identification}/{video_job.job_ref}/{os.path.basename(frame_path)}",
                        file_object=frame_file,
                        content_type='image/png'
                    )
                )
