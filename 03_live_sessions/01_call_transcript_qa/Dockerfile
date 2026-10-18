# Python version matches the project's venv (3.13)
FROM python:3.13-slim

# Don't write .pyc files; print logs straight away (no buffering)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install dependencies first, so this layer is cached until requirements.txt changes
COPY requirements.txt .
RUN pip install -r requirements.txt

# Then copy the app code (filtered by .dockerignore)
COPY . .

EXPOSE 8000

# 0.0.0.0 so the server is reachable from outside the container
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
