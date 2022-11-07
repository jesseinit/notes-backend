#!/bin/bash

WORKER_COUNT=$(nproc)

while !</dev/tcp/${DATABASE_HOST}/${DATABASE_PORT}; do 
    echo "Waiting for postgress listening..."
    sleep 0.1; 
done;
echo "PostgreSQL started"

echo Running Alembic Migrations.
alembic upgrade head

echo Starting API Server.
uvicorn main:app --reload --workers $WORKER_COUNT --host 0.0.0.0 --port 8022
