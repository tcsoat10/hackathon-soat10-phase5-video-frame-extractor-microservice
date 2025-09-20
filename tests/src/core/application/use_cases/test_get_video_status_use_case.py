import pytest
from unittest.mock import Mock

from src.core.application.use_cases.get_video_status import GetVideoStatusUseCase
from src.core.domain.dtos.video_frame_extractor.video_job_dto import VideoJobDTO
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.repositories.i_video_job_repository import IVideoJobRepository
from tests.factories.video_job_factory import VideoJobFactory


@pytest.fixture
def mock_video_job_repository():
    return Mock(spec=IVideoJobRepository)


@pytest.fixture
def get_video_status_use_case(mock_video_job_repository):
    return GetVideoStatusUseCase(video_job_repository=mock_video_job_repository)


def test_build_get_video_status_use_case(mock_video_job_repository):
    use_case = GetVideoStatusUseCase.build(video_job_repository=mock_video_job_repository)

    assert isinstance(use_case, GetVideoStatusUseCase)
    assert use_case._video_job_repository == mock_video_job_repository


@pytest.mark.asyncio
async def test_execute_get_video_status_use_case_success(get_video_status_use_case, mock_video_job_repository):
    video_job_entity = VideoJobFactory().to_entity()
    mock_video_job_repository.find_by_job_ref.return_value = video_job_entity

    result_dto = await get_video_status_use_case.execute(video_job_entity.job_ref)

    mock_video_job_repository.find_by_job_ref.assert_called_once_with(video_job_entity.job_ref)
    assert isinstance(result_dto, VideoJobDTO)
    assert result_dto.job_ref == video_job_entity.job_ref
    assert result_dto.status == video_job_entity.status


@pytest.mark.asyncio
async def test_execute_get_video_status_use_case_not_found(get_video_status_use_case, mock_video_job_repository):
    mock_video_job_repository.find_by_job_ref.return_value = None
    job_ref = "non_existent_job_ref"

    with pytest.raises(EntityNotFoundException) as exc_info:
        await get_video_status_use_case.execute(job_ref)

    mock_video_job_repository.find_by_job_ref.assert_called_once_with(job_ref)
    assert str(exc_info.value) == f"VideoJob com job_ref {job_ref} não encontrado."
