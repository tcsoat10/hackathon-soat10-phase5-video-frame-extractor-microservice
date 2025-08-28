import os

from dotenv import load_dotenv

load_dotenv()

# Configurações de ambiente
DEBUG = os.getenv("DEBUG", "true").lower() in ("true", "1")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # development, staging, production

# Configurações de servidor
SERVER_HOST = os.getenv("SERVER_HOST", "localhost")
SERVER_PORT = int(os.getenv("APP_PORT", 5000))

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

MERCADO_PAGO_ACCESS_TOKEN = os.getenv("MERCADO_PAGO_ACCESS_TOKEN")
MERCADO_PAGO_USER_ID = os.getenv('MERCADO_PAGO_USER_ID')
MERCADO_PAGO_POS_ID = os.getenv('MERCADO_PAGO_POS_ID')

WEBHOOK_URL = os.getenv('WEBHOOK_URL')
