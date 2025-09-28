import os
from kombu import Queue

task_serializer = 'json'
accept_content = ['json']
result_serializer = 'json'
timezone = 'UTC'
enable_utc = True
task_track_started = True

task_time_limit = 30 * 60
task_soft_time_limit = 25 * 60
default_retry_delay = 60
max_retries = 3

_env = os.environ.get('ENVIRONMENT', '').lower()
_suffix = '_dev' if _env == 'development' else ''

default_q = f'default{_suffix}'
extract_frames_q = f'extract_frames_queue{_suffix}'
notification_q = f'notification_queue{_suffix}'

task_default_queue = default_q
task_queues = (
    Queue(default_q),
    Queue(extract_frames_q),
    Queue(notification_q),
)
task_routes = {
    'src.infrastructure.tasks.video_tasks.extract_frames_task': {'queue': extract_frames_q},
    'src.infrastructure.tasks.notification_task.send_notification_task': {'queue': notification_q},
}

worker_prefetch_multiplier = 1
worker_max_tasks_per_child = 1000
worker_send_task_events = True
task_send_sent_event = True
worker_hijack_root_logger = False
worker_log_color = False

task_acks_late = True
task_result_expires = 3600
result_expires = 3600
broker_connection_retry_on_startup = True
broker_connection_retry = True
