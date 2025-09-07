import os
from celery import Celery
from celery.signals import worker_process_init

from src.config.database import connect_db 
from src.config.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_DEFAULT_REGION,
    SQS_QUEUE_NAME,
    ENVIRONMENT
)
 
def get_sqs_url():
    return "sqs://"

def get_redis_url():
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
    redis_auth = f":{REDIS_PASSWORD}@" if REDIS_PASSWORD else ""
    return f"redis://{redis_auth}{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
 
def get_message_broker():
    if ENVIRONMENT == 'production':
        if not all([AWS_ACCESS_KEY_ID, AWS_DEFAULT_REGION, AWS_SECRET_ACCESS_KEY, SQS_QUEUE_NAME]):
            raise ValueError("Missing AWS SQS configuration for production environment")

        return get_sqs_url()
    
    return get_redis_url()


celery_app = Celery(
    'video_frame_extractor_microservice',
    broker=get_message_broker(),
    backend=get_redis_url(),
    include=['src.infrastructure.tasks.video_tasks']
)
celery_app.config_from_object('src.config.celery_config')

@worker_process_init.connect
def init_worker(**kwargs):
    from src.core.containers import Container
    connect_db()
    Container()

celery_app.autodiscover_tasks([
    'src.infrastructure.tasks.video_tasks',
])
