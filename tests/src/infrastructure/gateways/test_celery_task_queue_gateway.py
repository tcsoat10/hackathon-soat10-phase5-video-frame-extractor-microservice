import pytest
from unittest.mock import Mock, patch

from celery import Celery

from src.infrastructure.gateways.celery_task_queue_gateway import CeleryTaskQueueGateway


@pytest.fixture
def mock_celery_app():
    return Mock(spec=Celery)


@pytest.fixture
def gateway(mock_celery_app):
    return CeleryTaskQueueGateway(celery_app=mock_celery_app)


def test_initialization(gateway, mock_celery_app):
    assert gateway._celery_app is mock_celery_app


def test_enqueue_video_processing_task(gateway, mock_celery_app):
    task_data = {"job_ref": "test_job_123", "video_path": "/path/to/video.mp4"}
    mock_task = Mock()
    mock_task.id = "some-task-id"
    mock_celery_app.send_task.return_value = mock_task

    task_id = gateway.enqueue_video_processing_task(task_data)

    mock_celery_app.send_task.assert_called_once_with(
        'src.infrastructure.tasks.video_tasks.extract_frames_task',
        args=[task_data]
    )
    assert task_id == "some-task-id"
