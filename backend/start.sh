#!/bin/bash
# Railway startup script

# Set Django settings module for production
if [ -z "$DJANGO_SETTINGS_MODULE" ]; then
    echo "DJANGO_SETTINGS_MODULE not set, defaulting to prod"
    export DJANGO_SETTINGS_MODULE="config.settings.prod"
else
    echo "Using DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
fi

# Use Railway's PORT or fallback to 8000
if [ -z "$PORT" ]; then
    echo "PORT environment variable not set, using 8000"
    export PORT=8000
else
    echo "Using PORT from environment: $PORT"
fi

# Debug: Print environment info
echo "Environment variables check:"
echo "  DATABASE_URL exists: $([ -n "$DATABASE_URL" ] && echo 'YES' || echo 'NO')"
echo "  CLERK_WEBHOOK_SECRET exists: $([ -n "$CLERK_WEBHOOK_SECRET" ] && echo 'YES' || echo 'NO')"

echo "Starting Gunicorn on 0.0.0.0:$PORT..."

# Run gunicorn
exec gunicorn config.wsgi \
    --bind "0.0.0.0:$PORT" \
    --workers 2 \
    --timeout 120 \
    --log-level info \
    --access-logfile - \
    --error-logfile -
