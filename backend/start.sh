#!/bin/bash
# Railway startup script

# Set default PORT if not provided
export PORT=${PORT:-8000}

echo "Starting Gunicorn on port $PORT..."

# Run gunicorn
exec gunicorn config.wsgi \
    --bind 0.0.0.0:${PORT} \
    --workers 2 \
    --timeout 120 \
    --log-level info \
    --access-logfile - \
    --error-logfile -
