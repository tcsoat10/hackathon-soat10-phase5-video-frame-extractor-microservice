# Task para enviar notificação callback sobre o status. Será registrado em outra fila.
from typing import Dict, Any
from dependency_injector.wiring import inject, Provide

from src.config.celery_app import celery_app
from src.core.containers import Container
from src.core.ports.gateways.callbacks.i_notification_gateway import INotificationGateway
from src.core.ports.repositories.i_video_job_repository import IVideoJobRepository

@celery_app.task(
    name='src.infrastructure.tasks.notification_task.send_notification_task',
    bind=True,
    acks_late=True,
)
@inject
def send_notification_task(
    self,
    task_data: Dict[str, Any],
    video_job_repository: IVideoJobRepository = Provide[Container.video_job_repository],
    notification_gateway: INotificationGateway = Provide[Container.notification_gateway],
):
    try:
        print(f"Iniciando task de notificação {self.request.id} com dados: {task_data}")
        job_ref = task_data.get("job_ref")
        if not job_ref:
            raise ValueError("job_ref is required in task_data")

        video_job = video_job_repository.find_by_job_ref(job_ref)
        if not video_job:
            raise ValueError(f"Video job with ref {job_ref} not found")

        notification_gateway.send_notification(
            video_job.notify_url,
            video_job.build_notification(detail=task_data.get("detail")),
        )
        print(f"Task de notificação {self.request.id} concluída com sucesso.")
        return {'status': 'success', 'job_ref': job_ref}
    except Exception as e:
        import traceback
        traceback.print_exc()
        
        print(f"Erro na task de notificação {self.request.id}: {e}")

        raise self.retry(exc=e, countdown=60)
