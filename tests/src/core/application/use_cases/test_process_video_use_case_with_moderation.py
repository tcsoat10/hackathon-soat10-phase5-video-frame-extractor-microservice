import pytest
from unittest.mock import Mock, patch
from src.core.application.use_cases.process_video_use_case import ProcessVideoUseCase
from src.core.domain.dtos.video_frame_extractor.process_video_task_dto import ProcessVideoTaskDTO
from src.core.domain.entities.video_job import VideoJob
from src.core.constants.video_job_status import VideoJobStatus


class TestProcessVideoUseCaseWithModeration:
    
    def test_should_reject_video_when_inappropriate_content_detected(self):
        # Arrange
        video_job_repository = Mock()
        storage_gateway = Mock()
        video_processor = Mock()
        notification_gateway = Mock()
        content_moderation_gateway = Mock()
        
        # Mock video job
        video_job = VideoJob(
            job_ref="test_job_123",
            client_identification="client_123",
            status=VideoJobStatus.QUEUED.status,
            bucket="test-bucket",
            video_path="videos",
            frames_path="frames"
        )
        
        video_job_repository.find_by_job_ref.return_value = video_job
        
        # Mock moderation result - inappropriate content
        content_moderation_gateway.moderate_video_content.return_value = {
            "is_appropriate": False,
            "confidence": 85.5,
            "labels": [
                {"name": "Explicit Nudity", "confidence": 85.5},
                {"name": "Adult Content", "confidence": 78.2}
            ],
            "job_id": "moderation_job_123"
        }
        
        use_case = ProcessVideoUseCase(
            video_job_repository=video_job_repository,
            storage_gateway=storage_gateway,
            video_processor=video_processor,
            notification_gateway=notification_gateway,
            content_moderation_gateway=content_moderation_gateway
        )
        
        dto = ProcessVideoTaskDTO(
            job_ref="test_job_123",
            client_identification="client_123",
            bucket="test-bucket",
            video_path="videos",
            frames_path="frames"
        )
        
        # Act
        result = use_case.execute(dto)
        
        # Assert
        assert result["status"] == VideoJobStatus.REJECTED.status
        assert "Explicit Nudity" in result["reason"]
        assert "Adult Content" in result["reason"]
        
        # Verify moderation was called
        content_moderation_gateway.moderate_video_content.assert_called_once_with(
            bucket="test-bucket",
            video_key="videos/client_123/test_job_123"
        )
        
        # Verify video job was rejected
        video_job_repository.save.assert_called()
        assert video_job.status == VideoJobStatus.REJECTED.status
        
        # Verify notification was sent
        notification_gateway.send_notification.assert_called_once()
        
        # Verify video processing was NOT called
        storage_gateway.download_object.assert_not_called()
        video_processor.extract_frames.assert_not_called()

    def test_should_continue_processing_when_content_is_appropriate(self):
        # Arrange
        video_job_repository = Mock()
        storage_gateway = Mock()
        video_processor = Mock()
        notification_gateway = Mock()
        content_moderation_gateway = Mock()
        
        # Mock video job
        video_job = VideoJob(
            job_ref="test_job_456",
            client_identification="client_456",
            status=VideoJobStatus.QUEUED.status,
            bucket="test-bucket",
            video_path="videos",
            frames_path="frames"
        )
        
        video_job_repository.find_by_job_ref.return_value = video_job
        
        # Mock moderation result - appropriate content
        content_moderation_gateway.moderate_video_content.return_value = {
            "is_appropriate": True,
            "confidence": 0.0,
            "labels": [],
            "job_id": "moderation_job_456"
        }
        
        # Mock other dependencies
        storage_gateway.download_object.return_value = b"fake_video_data"
        video_processor.extract_frames.return_value = ["/tmp/frame1.png", "/tmp/frame2.png"]
        
        use_case = ProcessVideoUseCase(
            video_job_repository=video_job_repository,
            storage_gateway=storage_gateway,
            video_processor=video_processor,
            notification_gateway=notification_gateway,
            content_moderation_gateway=content_moderation_gateway
        )
        
        dto = ProcessVideoTaskDTO(
            job_ref="test_job_456",
            client_identification="client_456",
            bucket="test-bucket",
            video_path="videos",
            frames_path="frames"
        )
        
        # Act
        with patch("builtins.open", create=True) as mock_open, \
             patch("tempfile.TemporaryDirectory") as mock_temp_dir, \
             patch("os.path.join") as mock_join, \
             patch("os.path.basename") as mock_basename:
            
            mock_temp_dir.return_value.__enter__.return_value = "/tmp"
            mock_join.return_value = "/tmp/input_video"
            mock_basename.side_effect = lambda x: x.split("/")[-1]
            
            result = use_case.execute(dto)
        
        # Assert
        assert result["job_ref"] == "test_job_456"
        assert result["client_identification"] == "client_456"
        assert result["bucket"] == "test-bucket"
        
        # Verify moderation was called
        content_moderation_gateway.moderate_video_content.assert_called_once()
        
        # Verify video processing continued
        storage_gateway.download_object.assert_called_once()
        video_processor.extract_frames.assert_called_once()
        
        # Verify video job was completed
        assert video_job.status == VideoJobStatus.COMPLETED.status