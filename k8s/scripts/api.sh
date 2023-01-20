#!/bin/bash

let WORKER_COUNT=2*$(nproc)+1

echo "Starting API Server."

if [[ "$ENV" == "production" ]]
then
    echo "Starting Production"
    uvicorn main:app --workers $WORKER_COUNT --host 0.0.0.0 --port 8022
elif [[ "$ENV" == "app-runner" ]]
then
    echo "Starting Application on App Runner"
    echo "Running Database Migrations."
    alembic upgrade head
    echo "Completed Database Migrations."
    uvicorn main:app --workers $WORKER_COUNT --host 0.0.0.0 --port 8022
else
    echo "Starting Development"
    uvicorn main:app --reload --host 0.0.0.0 --port 8022
fi
