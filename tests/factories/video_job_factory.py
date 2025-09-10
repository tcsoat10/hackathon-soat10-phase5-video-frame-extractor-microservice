from bson import ObjectId
import factory
from factory.mongoengine import MongoEngineFactory
from faker import Faker
from src.core.constants.video_job_status import VideoJobStatus
from src.infrastructure.repositories.mongoengine.models.video_job_model import VideoJobModel

fake = Faker()

class VideoJobFactory(MongoEngineFactory):
    class Meta:
        model = VideoJobModel

    id = factory.LazyFunction(lambda: ObjectId())
    job_ref = factory.LazyFunction(lambda: f"job_{fake.uuid4()}")
    client_identification = factory.LazyFunction(lambda: fake.md5())
    status = factory.LazyFunction(lambda: str(VideoJobStatus.PENDING))
    bucket = "test-bucket"
    video_path = factory.LazyAttribute(lambda o: f"videos/{o.job_ref}/video.mp4")
    frames_path = factory.LazyAttribute(lambda o: f"frames/{o.job_ref}/")
    notify_url = factory.LazyFunction(fake.url)
    config = {}
    error_message = None
    created_at = factory.LazyFunction(fake.date_time_this_decade)
    updated_at = factory.LazyFunction(fake.date_time_this_decade)
    inactivated_at = None
