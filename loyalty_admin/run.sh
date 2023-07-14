#!/usr/bin/env bash

set -e

# Start server
echo "Starting server"
gunicorn --worker-class=uvicorn.workers.UvicornWorker --workers=1 -b ${LADMIN_APP__HOST}:${LADMIN_APP__PORT} app:app
