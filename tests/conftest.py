import os
import pytest
from fastapi.testclient import TestClient
from typing import Generator
import mongomock
from mongoengine import connect, disconnect
from unittest.mock import patch

from src.app import app
from src.core.containers import Container


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment"""    
    # Set test environment variables
    os.environ['MONGO_DB'] = 'test_video_frame_extractor_microservice'
    os.environ['MONGO_HOST'] = 'localhost'
    os.environ['MONGO_PORT'] = '27017'
    os.environ['MONGO_USER'] = ''
    os.environ['MONGO_PASSWORD'] = ''
    os.environ['VIDEO_FRAME_EXTRACTOR_MICROSERVICE_X_API_KEY'] = 'test_api_key'

    # Celery config celery for tests
    os.environ['CELERY_TASK_ALWAYS_EAGER'] = 'True'
    os.environ['CELERY_BROKER_URL'] = 'memory://'
    os.environ['CELERY_RESULT_BACKEND'] = 'rpc://'
    os.environ['CELERY_NOTIFICATION_MAX_RETRIES'] = '2'
    os.environ['CELERY_NOTIFICATION_RETRY_DELAY_SECONDS'] = '0'

    yield

    try:
        disconnect(alias='test')
        disconnect(alias='default')
    except Exception:
        pass


@pytest.fixture(scope="function")
def mongo_db():
    """
    Fixture para configurar um banco de dados MongoDB mock para testes.
    """
    try:
        disconnect(alias='test')
    except Exception:
        pass

    connect(
        db='test_video_frame_extractor_microservice',
        host='localhost',
        port=27017,
        mongo_client_class=mongomock.MongoClient,
        alias='default'
    )
    
    yield mongomock.MongoClient('localhost', 27017)

    try:
        disconnect(alias='default')
    except Exception:
        pass


@pytest.fixture(scope="function")
def client(mongo_db) -> Generator[TestClient, None, None]:
    """
    Cria um cliente de teste para a aplicação.
    """
    with patch('src.config.database.connect_db') as mock_connect:
        with patch('src.config.database.disconnect_db') as mock_disconnect:
            mock_connect.return_value = None
            mock_disconnect.return_value = None
            
            headers = {"x-api-key": "test_api_key"}
            with TestClient(app, headers=headers) as test_client:
                yield test_client


@pytest.fixture(scope="function")
def container(mongo_db) -> Generator[Container, None, None]:
    """
    Cria um container de dependências para testes.
    """
    container = Container()
    container.wire(modules=[
        "tests.src.infrastructure.repositories.mongoengine.test_video_job_repository",
    ])
    yield container
    container.unwire()

def get_headers():
    return { "x-api-key": "test_api_key" }

@pytest.fixture(autouse=True)
def clean_database(mongo_db):
    try:
        from src.infrastructure.repositories.mongoengine.models.video_job_model import VideoJobModel

        VideoJobModel._get_db = lambda: mongo_db['test_video_frame_extractor_microservice']
        
        VideoJobModel.objects.delete()
    except Exception as e:
        print(f"Error cleaning database: {e}")
    
    yield

    try:
        VideoJobModel.objects.delete()
    except Exception as e:
        print(f"Error cleaning database after test: {e}")
