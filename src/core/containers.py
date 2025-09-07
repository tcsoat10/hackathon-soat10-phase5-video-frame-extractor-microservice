from dependency_injector import containers, providers
from src.config.celery_app import celery_app

from src.config.database import get_db
from src.core.shared.identity_map import IdentityMap
from src.infrastructure.repositories.mongoengine.video_job_repository import MongoVideoJobRepository
from src.core.ports.repositories.i_video_job_repository import IVideoJobRepository
from src.infrastructure.gateways.local_object_storage_gateway import LocalObjectStorageGateway
from src.infrastructure.gateways.celery_task_queue_gateway import CeleryTaskQueueGateway
from src.core.ports.cloud.object_storage_gateway import ObjectStorageGateway
from src.core.ports.tasks.i_task_queue_gateway import ITaskQueueGateway
from src.infrastructure.video.ffmpeg_wrapper import FFmpegWrapper
from src.presentation.api.v1.controllers.video_controller import VideoController


class Container(containers.DeclarativeContainer):    
    wiring_config = containers.WiringConfiguration(modules=[
        "src.presentation.api.v1.routes.video_frame_extractor",
        "src.infrastructure.tasks.video_tasks",
    ])

    identity_map = providers.Singleton(IdentityMap)
    db_connection = providers.Resource(get_db)
    
    print(f"DB_CONNECTION IS: {db_connection}")
    
    celery_app_provider = providers.Object(celery_app)

    object_storage_gateway: providers.Singleton[ObjectStorageGateway] = providers.Singleton(
        LocalObjectStorageGateway # TODO: Substituir por implementação do bucket S3
    )
    task_queue_gateway: providers.Singleton[ITaskQueueGateway] = providers.Singleton(
        CeleryTaskQueueGateway,
        celery_app=celery_app_provider
    )
    ffmpeg_wrapper = providers.Factory(FFmpegWrapper)

    video_job_repository: providers.Factory[IVideoJobRepository] = providers.Factory(
        MongoVideoJobRepository
    )

    video_controller = providers.Factory(
        VideoController,
        video_job_repository=video_job_repository,
        storage_gateway=object_storage_gateway,
        task_gateway=task_queue_gateway
    )
