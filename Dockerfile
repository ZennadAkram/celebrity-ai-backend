FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=celebrity_ai.settings

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt /app/
COPY service-account.json /app/service-account.json
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/






CMD HOME=/root python3 manage.py runserver 0.0.0.0:8000 --noreload
