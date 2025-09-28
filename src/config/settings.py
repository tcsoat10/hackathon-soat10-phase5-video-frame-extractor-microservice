import os
import logging

from dotenv import load_dotenv

load_dotenv()

def set_logging_level():    
    logging_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    log_level = os.getenv("LOG_LEVEL", "INFO")
    
    if log_level not in logging_levels:
        raise ValueError(f"Invalid log level: {log_level}")
    
    return logging_levels.get(log_level, logging.INFO)

# Configurações de ambiente
DEBUG = os.getenv("DEBUG", "true").lower() in ("true", "1")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # development, staging, production

# Configurações de servidor
SERVER_HOST = os.getenv("SERVER_HOST", "localhost")
SERVER_PORT = int(os.getenv("APP_PORT", 5000))

LOG_LEVEL = set_logging_level()

ZIPPER_SERVICE_URL = os.getenv("ZIPPER_SERVICE_URL")
ZIPPER_SERVICE_X_API_KEY = os.getenv("ZIPPER_SERVICE_X_API_KEY")

STORAGE_BUCKET = os.getenv("STORAGE_BUCKET", "default-bucket")
STORAGE_VIDEO_PATH = os.getenv("STORAGE_VIDEO_PATH", "default-path-video")
STORAGE_FRAMES_PATH = os.getenv("STORAGE_FRAMES_PATH", "default-path-frames")

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN')

SQS_QUEUE_NAME = os.getenv('SQS_QUEUE_NAME', 'extract_frames_queue')

if ENVIRONMENT == 'development':
    SQS_QUEUE_NAME = f"{SQS_QUEUE_NAME}-dev"
elif ENVIRONMENT == 'production':
    SQS_QUEUE_NAME = f"{SQS_QUEUE_NAME}-prod"

FRAMES_PER_SECOND = os.getenv('FRAMES_PER_SECOND', '1')
