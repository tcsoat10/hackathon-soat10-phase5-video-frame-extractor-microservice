#!/bin/sh
set -e

echo "Waiting for database to be ready..."

MAX_RETRIES=3000
COUNT=0

while ! nc -z $MONGO_HOST $MONGO_PORT; do
  sleep 2
  COUNT=$((COUNT+1))
  if [ $COUNT -ge $MAX_RETRIES ]; then
    echo "Database is not ready after $MAX_RETRIES attempts, exiting..."
    exit 1
  fi
done

echo "Database is up, applying migrations..."

poetry run python ./src/config/init_db/run_migrations.py
echo "Migrations applied successfully."