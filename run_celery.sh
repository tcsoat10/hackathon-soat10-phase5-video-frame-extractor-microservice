#!/bin/bash
set -e

# Importa o worker para registrar os signals do Celery
export PYTHONPATH=$PYTHONPATH:/app

echo "Starting Celery with command: $@"

# Executa o comando passado como argumento (worker ou beat)
poetry run celery -A src.config.celery_app:celery_app "$@"