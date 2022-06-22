#!/bin/bash

echo Running Alembic Migrations.
alembic upgrade head

echo Starting API Server.
uvicorn main:app --reload --workers 1 --reload --host 0.0.0.0 --port 8022
