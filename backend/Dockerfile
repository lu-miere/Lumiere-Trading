FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    libpq5 && \
    pip install poetry && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false

RUN poetry install --only main


COPY . /app/

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE="api.settings"

CMD ["python", "-m", "gunicorn", "-b", "0.0.0.0:8000", "--workers", "4", "api.wsgi:application"]