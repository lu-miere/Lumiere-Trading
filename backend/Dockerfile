FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ----------------------------------------------------------------------
# 1. Install dependencies and system libraries in one stage
# This simplifies the build and eliminates multi-stage copying issues.
# ----------------------------------------------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    # Install runtime PostgreSQL client library
    libpq5 && \
    pip install poetry && \
    rm -rf /var/lib/apt/lists/*

# Copy configuration files (This assumes Gunicorn is now in pyproject.toml and poetry.lock)
COPY pyproject.toml poetry.lock /app/

# Install dependencies directly into the system site-packages (no virtual env)
RUN poetry config virtualenvs.create false
# Install only production dependencies
RUN poetry install --only main

# ----------------------------------------------------------------------
# 2. Application Code and Command
# ----------------------------------------------------------------------

# Copy the application code
COPY . /app/

EXPOSE 8000

# Set settings module for Django (Used by manage.py, but Gunicorn CMD is primary)
ENV DJANGO_SETTINGS_MODULE="api.settings"

# FINAL COMMAND: Runs Gunicorn as a Python module using the confirmed WSGI path.
CMD ["python", "-m", "gunicorn", "-b", "0.0.0.0:8000", "--workers", "4", "api.wsgi:application"]