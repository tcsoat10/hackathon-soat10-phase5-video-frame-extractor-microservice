from typing import Dict, Any
from celery import Celery

from src.core.ports.tasks.i_task_queue_gateway import ITaskQueueGateway

class CeleryTaskQueueGateway(ITaskQueueGateway):

    def __init__(self, celery_app: Celery):
        self._celery_app = celery_app

    def enqueue_video_processing_task(self, task_data: Dict[str, Any]) -> str:
        task = self._celery_app.send_task(
            'src.infrastructure.tasks.video_tasks.extract_frames_task',
            args=[task_data],
            queue='extract_frames_queue'
        )
        return task.id
    
    def notification_status_callback(self, task_data: Dict[str, Any]) -> str:
        task = self._celery_app.send_task(
            'src.infrastructure.tasks.notification_task.send_notification_task',
            args=[task_data],
            queue='notification_queue'
        )
        return task.id

__all__ = ["CeleryTaskQueueGateway"]
