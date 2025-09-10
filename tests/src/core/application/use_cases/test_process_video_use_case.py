
from unittest.mock import MagicMock, Mock, patch
from src.core.domain.dtos.video_frame_extractor.process_video_task_dto import ProcessVideoTaskDTO
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from tests.factories.video_job_factory import VideoJobFactory
from src.core.application.use_cases.process_video_use_case import ProcessVideoUseCase

@patch('src.infrastructure.repositories.mongoengine.video_job_repository.MongoVideoJobRepository')
@patch('src.infrastructure.video.ffmpeg_wrapper.FFmpegWrapper')
@patch('src.infrastructure.gateways.s3_storage_gateway.S3StorageGateway')
def test_process_video_use_case_success(mock_storage_gateway, mock_ffmpeg_wrapper, mock_video_job_repository):
    mock_storage_gateway.download_object.return_value = b"video content"
    mock_storage_gateway.upload_objects_bulk.return_value = None
    mock_ffmpeg_wrapper.extract_frames.return_value = ["frame1.jpg", "frame2.jpg"]
  
    video_job = VideoJobFactory()
    mock_video_job_repository.find_by_job_ref.return_value = video_job.to_entity()
    
    dto = ProcessVideoTaskDTO(
        job_ref=video_job.job_ref,
        client_identification=video_job.client_identification,
        bucket=video_job.bucket,
        video_path=video_job.video_path,
        frames_path=video_job.frames_path,
        notify_url=video_job.notify_url,
        config=video_job.config,
    )

    use_case = ProcessVideoUseCase(
        video_job_repository=mock_video_job_repository,
        storage_gateway=mock_storage_gateway,
        video_processor=mock_ffmpeg_wrapper
    )
    
    use_case._upload_frames_in_bulk = MagicMock()

    result = use_case.execute(dto)

    assert result["job_ref"] == video_job.job_ref
    assert result["client_identification"] == video_job.client_identification
    assert result["bucket"] == video_job.bucket
    assert result["notify_url"] == video_job.notify_url
    
@patch('src.infrastructure.repositories.mongoengine.video_job_repository.MongoVideoJobRepository')
@patch('src.infrastructure.video.ffmpeg_wrapper.FFmpegWrapper')
@patch('src.infrastructure.gateways.s3_storage_gateway.S3StorageGateway')
def test_process_video_use_case_video_job_not_found(mock_storage_gateway, mock_ffmpeg_wrapper, mock_video_job_repository):
    mock_video_job_repository.find_by_job_ref.return_value = None
    
    dto = ProcessVideoTaskDTO(
        job_ref="nonexistent_job_ref",
        client_identification="client1",
        bucket="bucket1",
        video_path="path/to/video",
        frames_path="path/to/frames",
        notify_url="http://notify.url",
        config={}
    )

    use_case = ProcessVideoUseCase(
        video_job_repository=mock_video_job_repository,
        storage_gateway=mock_storage_gateway,
        video_processor=mock_ffmpeg_wrapper
    )

    try:
        use_case.execute(dto)
        assert False, "Expected EntityNotFoundException"
    except EntityNotFoundException as e:
        assert str(e) == "VideoJob com job_ref nonexistent_job_ref não encontrado."
