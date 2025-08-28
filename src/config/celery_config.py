import os
from celery import Celery
from kombu import Queue

REDIS_HOST = os.getenv('REDIS_HOST', 'video-frame-extractor-microservice-redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

def get_message_broker():
    if ENVIRONMENT == 'production':
        AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
        AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
        AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
        SQS_QUEUE_NAME = os.getenv('SQS_QUEUE_NAME', 'video-frame-extractor-queue')

        if not all([AWS_ACCESS_KEY, AWS_SECRET_KEY, SQS_QUEUE_NAME]):
            raise ValueError("Missing AWS SQS configuration for production environment")

        return f"sqs://{AWS_ACCESS_KEY}:{AWS_SECRET_KEY}@{AWS_REGION}/{SQS_QUEUE_NAME}"
    else:
        redis_auth = f":{REDIS_PASSWORD}@" if REDIS_PASSWORD else ""
        return f"redis://{redis_auth}{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

MESSAGE_BROKER = get_message_broker()
RESULT_BACKEND = MESSAGE_BROKER if ENVIRONMENT != 'production' else f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

print(f"Celery conectando no Redis: {MESSAGE_BROKER}")

celery_app = Celery(
    'video_frame_extractor_microservice',
    broker=MESSAGE_BROKER,
    backend=RESULT_BACKEND,
    include=[]
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutos
    task_soft_time_limit=25 * 60,  # 25 minutos
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    task_routes={
        'extract_frames_task': {'queue': 'extract_frames_queue'},
        'send_zip_frames_notification_task': {'queue': 'zip_frames_notifications_queue'},
    },
    task_default_queue='default',
    task_queues=(
        Queue('default'),
        Queue('extract_frames_queue'),
        Queue('zip_frames_notifications_queue'),
    ),
    task_acks_late=True,
    worker_send_task_events=True,
    task_send_sent_event=True,
    worker_hijack_root_logger=False,
    worker_log_color=False,
    task_result_expires=3600,  # 1 hora
    result_expires=3600,
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
)

celery_app.autodiscover_tasks()
