#!/bin/bash

set -e

echo "Attempting to run Database Migrations."

while ! nc -z $DATABASE_HOST $DATABASE_PORT; do 
    echo "Waiting for Database to Start..."
    sleep 0.1; 
done;

echo "PostgreSQL started"
echo "Running Database Migrations."
alembic upgrade head
echo "Completed Database Migrations."
