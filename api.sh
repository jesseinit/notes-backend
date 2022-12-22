#!/bin/bash

let WORKER_COUNT=2*$(nproc)+1

while ! nc -z $DATABASE_HOST $DATABASE_PORT; do 
    echo "Waiting for postgress listening..."
    sleep 0.1; 
done;
echo "Database Up"

echo Starting API Server.

if [[ "$ENV" == "production" ]]
then
    echo "Starting Production"
    uvicorn main:app --workers $WORKER_COUNT --host 0.0.0.0 --port 8022
else
    echo "Starting Development"
    uvicorn main:app --reload --host 0.0.0.0 --port 8022
fi
