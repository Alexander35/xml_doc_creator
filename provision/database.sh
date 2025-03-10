#!/bin/bash

echo "Waiting for PostgreSQL..."

export $(grep -v '^#' /conf/.env | xargs)

until pg_isready -h postgres -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  echo "PostgreSQL is unavailable - try to reconnect in  in 3 sec..."
  sleep 3
done

echo "PostgreSQL is ready!"
echo "Running migrations..."

alembic upgrade head

echo "All Migrations are complete!"
