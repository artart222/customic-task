# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Prevents Python from buffering output
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies (for Pillow, etc.)
RUN apt-get update && apt-get install -y \
    libjpeg-dev zlib1g-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source
COPY . .

# Expose Django dev port
EXPOSE 8000

# Default command (overridden by compose services)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
