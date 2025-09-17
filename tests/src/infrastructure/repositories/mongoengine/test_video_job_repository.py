from bson import ObjectId
import pytest
from unittest.mock import patch

from src.core.constants.video_job_status import VideoJobStatus
from src.core.domain.entities.video_job import VideoJob
from src.core.ports.repositories.i_video_job_repository import IVideoJobRepository
from src.infrastructure.repositories.mongoengine.video_job_repository import MongoVideoJobRepository
from datetime import timedelta
from src.infrastructure.repositories.mongoengine.models.video_job_model import VideoJobModel
from tests.factories.video_job_factory import VideoJobFactory


class TestMongoVideoJobRepository:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.video_job_repository: IVideoJobRepository = MongoVideoJobRepository()
        self.clean_database()

    def clean_database(self):
        try:
            VideoJobModel.drop_collection()
        except Exception:
            pass

    @patch('src.infrastructure.repositories.mongoengine.video_job_repository.uuid4', return_value='a9b8c7d6-e5f4-3210-9876-543210fedcba')
    def test_save_new_video_job_with_patched_uuid(self, mock_uuid4):
        video_job = VideoJob(
            job_ref='',
            status=VideoJobStatus.PENDING.status,
            client_identification="test_client",
            bucket="test_bucket",
            video_path="test_video_path",
            frames_path="test_frames_path",
            notify_url="test_notify_url",
        )
        saved = self.video_job_repository.save(video_job)

        assert saved.id is not None
        assert saved.client_identification == 'test_client'
        assert saved.job_ref == 'a9b8c7d6-e5f4-3210-9876-543210fedcba'
        assert saved.video_path == "test_video_path"
        assert saved.frames_path == "test_frames_path"
        assert saved.notify_url == "test_notify_url"
        assert saved.status == 'PENDING'
        assert saved.created_at is not None
        assert saved.updated_at is not None
        assert saved.error_message is None
        assert saved.inactivated_at is None

    @patch('src.infrastructure.repositories.mongoengine.video_job_repository.uuid4', return_value='11111111-2222-3333-4444-555555555555')
    def test_update_existing_video_job(self, mock_uuid4):
        # create initial
        video_job = VideoJob(
            job_ref='',
            status=VideoJobStatus.PENDING.status,
            client_identification="clientupd",
            bucket="b",
            video_path="vpath",
            frames_path="fpath",
            notify_url="nurl",
        )
        saved = self.video_job_repository.save(video_job)

        saved.status = VideoJobStatus.PROCESSING.status.upper()
        saved.error_message = "an error occurred"
        saved.updated_at = saved.updated_at + timedelta(seconds=5)

        updated = self.video_job_repository.save(saved)

        assert updated.id == saved.id
        assert updated.job_ref == saved.job_ref
        assert updated.status == "PROCESSING"
        assert updated.error_message == "an error occurred"
        assert updated.updated_at is not None
        assert updated.updated_at != updated.created_at

    @patch('src.infrastructure.repositories.mongoengine.video_job_repository.uuid4', return_value='deadbeef-dead-beef-dead-beefdeadbeef')
    def test_find_by_job_ref_and_get_by_id(self, mock_uuid4):
        video_job = VideoJob(
            job_ref='',
            status=VideoJobStatus.PENDING.status,
            client_identification="finder",
            bucket="buck",
            video_path="v",
            frames_path="f",
            notify_url="n",
        )
        saved = self.video_job_repository.save(video_job)

        found_by_ref = self.video_job_repository.find_by_job_ref(saved.job_ref)
        found_by_id = self.video_job_repository.get_by_id(saved.id)

        assert found_by_ref is not None
        assert found_by_ref.id == saved.id
        assert found_by_ref.job_ref == saved.job_ref

        assert found_by_id is not None
        assert found_by_id.job_ref == saved.job_ref
        assert found_by_id.id == saved.id

    def test_get_by_id_nonexistent_video_job(self):
        nonexistent_id = ObjectId()
        found = self.video_job_repository.get_by_id(nonexistent_id)
        assert found is None

    def test_find_by_job_ref_nonexistent_video_job(self):
        nonexistent_job_ref = 'nonexistent_job_ref'
        found = self.video_job_repository.find_by_job_ref(nonexistent_job_ref)
        assert found is None

    def test_get_by_id_success(self):
        video_job = VideoJobFactory()

        found = self.video_job_repository.get_by_id(video_job.id)
        
        assert found.id == video_job.id
        assert found.job_ref == video_job.job_ref
        assert found.status == video_job.status
