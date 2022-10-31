#!/bin/bash

WORKER_COUNT=$(nproc)

echo "Waiting for postgres to get up and running..."
# while ! nc -z notes-db 5432; do
#   # where the postgres_container is the hos, in my case, it is a Docker container.
#   # You can use localhost for example in case your database is running locally.
#   echo "waiting for postgress listening..."
#   sleep 0.1
# done
while !</dev/tcp/notes-db/5432; do 
    echo "waiting for postgress listening..."
    sleep 0.1; 
done;
echo "PostgreSQL started"

echo Running Alembic Migrations.
alembic upgrade head

echo Starting API Server.
uvicorn main:app --reload --workers $WORKER_COUNT --reload --host 0.0.0.0 --port 8022
