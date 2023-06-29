#!/usr/bin/env bash

set -e

# Start server
echo "Starting server"
gunicorn --worker-class=uvicorn.workers.UvicornWorker --workers=4 -b ${LA_APP_HOST}:${LA_APP_PORT} src.app:app
