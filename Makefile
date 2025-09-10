poetry_install_dev:
	poetry install --with test --sync

poetry_install:
	poetry install --sync

build:
	docker compose build

up:
	docker compose up -d

up_build:
	docker compose up -d --build

down:
	docker compose down --remove-orphans

migrate_db:
	poetry run python ./src/config/init_db/run_migrations.py

dev:
	@echo "Starting MongoDB and Redis containers..."
	@docker compose up -d video-frame-extractor-microservice-mongodb video-frame-extractor-microservice-redis \
	celery-worker celery-beat celery-flower
	@echo "Waiting for services to be ready..."
	@sleep 5
	@echo "Applying migrations..."
	@MONGO_HOST=localhost MONGO_PORT=27017 REDIS_HOST=localhost ./src/config/init_db/init_db.sh
	@echo "Starting Uvicorn..."
	@echo "Flower disponível em: http://localhost:5555"
	@trap 'docker compose down --remove-orphans' INT TERM EXIT; \
	MONGO_HOST=localhost MONGO_PORT=27017 REDIS_HOST=localhost uvicorn src.app:app --reload --host 0.0.0.0 --port 8001

dev_full:
	@echo "Starting all services with Flower..."
	@docker compose up -d
	@echo "Aguardando todos os serviços iniciarem..."
	@sleep 20
	@echo ""
	@echo "Serviços disponíveis:"
	@echo "- API: http://localhost:8001"
	@echo "- Flower: http://localhost:5555"
	@echo "- MongoDB: localhost:27017"
	@echo "- Redis: localhost:6379"

test_watch:
	ENV=test ptw --runner 'pytest --ff $(extra)'

test_parallel:
	ENV=test pytest --cov=src --numprocesses auto --dist loadfile --max-worker-restart 0 $(extra)

test_last_failed:
	ENV=test ptw --runner 'pytest --ff --lf $(extra)'

test_coverage:
	coverage report --omit='tests/*,src/config/*,src/config/**,*/dependency_injector/*'

test_coverage_xml:
	coverage xml --omit='tests/*,src/config/*,src/config/**,*/dependency_injector/*'

celery_worker:
	PYTHONPATH=. poetry run celery -A src.config.celery_app worker --loglevel=info

celery_beat:
	PYTHONPATH=. poetry run celery -A src.config.celery_app beat --loglevel=info

celery_flower:
	PYTHONPATH=. poetry run celery -A src.config.celery_app flower --port=5555

celery_flower_with_auth:
	PYTHONPATH=. poetry run celery -A src.config.celery_app flower --port=5555 --basic_auth=admin:secret123

flower_logs:
	docker logs -f video-frame-extractor-microservice-celery-flower

celery_logs:
	docker logs -f video-frame-extractor-microservice-celery-worker

redis_cli:
	docker exec -it video-frame-extractor-microservice-redis redis-cli

monitor_tasks:
	@echo "Monitorando tasks do Celery..."
	@echo "Flower: http://localhost:5555"
	@echo "Logs do worker:"
	@make celery_logs
