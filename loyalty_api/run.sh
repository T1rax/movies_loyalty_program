#!/usr/bin/env bash

set -e

# DB Yoyo migrations
echo "Apply DB migrations"
yoyo apply --database ${DATABASE_URL} ./migrations -b
echo "DB Migrations applied"

# Start server
echo "Starting server"
gunicorn --worker-class=uvicorn.workers.UvicornWorker --workers=4 -b ${LA_APP_HOST}:${LA_APP_PORT} src.app:app
