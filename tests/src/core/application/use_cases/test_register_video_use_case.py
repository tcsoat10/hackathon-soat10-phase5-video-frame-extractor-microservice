import pytest
from unittest.mock import ANY, Mock, AsyncMock, call

from fastapi import UploadFile

from src.core.application.use_cases.register_video_use_case import RegisterVideoUseCase
from src.core.domain.dtos.video_frame_extractor.register_video_dto import RegisterVideoDTO
from src.core.domain.entities.video_job import VideoJob
from src.core.ports.repositories.i_video_job_repository import IVideoJobRepository
from src.core.ports.cloud.object_storage_gateway import ObjectStorageGateway
from src.core.ports.tasks.i_task_queue_gateway import ITaskQueueGateway


@pytest.fixture
def mock_video_job_repository():
    return Mock(spec=IVideoJobRepository)


@pytest.fixture
def mock_storage_gateway():
    return Mock(spec=ObjectStorageGateway)


@pytest.fixture
def mock_task_gateway():
    return Mock(spec=ITaskQueueGateway)


@pytest.fixture
def register_video_use_case(
    mock_video_job_repository, mock_storage_gateway, mock_task_gateway
):
    return RegisterVideoUseCase(
        video_job_repository=mock_video_job_repository,
        storage_gateway=mock_storage_gateway,
        task_gateway=mock_task_gateway,
    )

def test_build_register_video_use_case(
    mock_video_job_repository,
    mock_storage_gateway,
    mock_task_gateway,
):
    use_case = RegisterVideoUseCase.build(
        video_job_repository=mock_video_job_repository,
        storage_gateway=mock_storage_gateway,
        task_gateway=mock_task_gateway,
    )

    assert isinstance(use_case, RegisterVideoUseCase)
    assert use_case._video_job_repository == mock_video_job_repository
    assert use_case._storage_gateway == mock_storage_gateway
    assert use_case._task_gateway == mock_task_gateway

@pytest.mark.asyncio
async def test_execute_register_video_use_case(
    register_video_use_case,
    mock_video_job_repository,
    mock_storage_gateway,
    mock_task_gateway,
):
    mock_file = AsyncMock(spec=UploadFile)
    mock_file.read.return_value = b"fake video content"
    mock_file.content_type = "video/mp4"

    dto = RegisterVideoDTO(
        video_file=mock_file,
        client_identification="test_client",
        notify_url="http://test.com/notify",
    )

    saved_job = Mock(spec=VideoJob)
    saved_job.job_ref = "some-uuid"
    saved_job.client_identification = "test_client"
    saved_job.bucket = "test-bucket"
    saved_job.video_path = "videos"
    saved_job.frames_path = "frames"
    saved_job.notify_url = "http://test.com/notify"
    saved_job.config = {}
    mock_video_job_repository.save.return_value = saved_job

    result_job = await register_video_use_case.execute(dto)

    assert mock_video_job_repository.save.call_count == 2
    mock_storage_gateway.upload_object.assert_called_once()
    mock_task_gateway.enqueue_video_processing_task.assert_called_once()

    assert result_job == saved_job

@pytest.mark.asyncio
async def test_execute_register_video_use_case_with_error(
    register_video_use_case,
    mock_video_job_repository,
    mock_storage_gateway,
    mock_task_gateway,
):
    mock_file = AsyncMock(spec=UploadFile)
    mock_file.read.return_value = b"fake video content"
    mock_file.content_type = "video/mp4"

    dto = RegisterVideoDTO(
        video_file=mock_file,
        client_identification="test_client",
        notify_url="http://test.com/notify",
    )

    mock_video_job_repository.save.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        await register_video_use_case.execute(dto)

    assert mock_video_job_repository.save.call_count == 1

    mock_video_job_repository.save.assert_called_once()
    mock_storage_gateway.upload_object.assert_not_called()
    mock_task_gateway.enqueue_video_processing_task.assert_not_called()
