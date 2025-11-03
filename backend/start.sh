#!/bin/bash
# Railway startup script

# Use Railway's PORT or fallback to 8000
if [ -z "$PORT" ]; then
    echo "PORT environment variable not set, using 8000"
    export PORT=8000
else
    echo "Using PORT from environment: $PORT"
fi

echo "Starting Gunicorn on 0.0.0.0:$PORT..."

# Run gunicorn
exec gunicorn config.wsgi \
    --bind "0.0.0.0:$PORT" \
    --workers 2 \
    --timeout 120 \
    --log-level info \
    --access-logfile - \
    --error-logfile -
