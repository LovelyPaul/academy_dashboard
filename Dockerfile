# Multi-stage Dockerfile for Django + React deployment on Railway

# Stage 1: Build React frontend
FROM node:18-alpine AS frontend-build
WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./
RUN npm ci --legacy-peer-deps

# Copy frontend source and build
COPY frontend/ ./
RUN npm run build

# Stage 2: Python backend with static files
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt /app/backend/
RUN pip install --upgrade pip && \
    pip install -r /app/backend/requirements.txt

# Copy backend application
COPY backend/ /app/backend/

# Copy frontend build from previous stage
COPY --from=frontend-build /app/frontend/build /app/frontend/build

# Set working directory to backend
WORKDIR /app/backend

# Collect static files
RUN python manage.py collectstatic --noinput --clear || true

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", "config.wsgi:application"]
