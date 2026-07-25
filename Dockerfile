# Shop Discord Bot — Dockerfile
FROM python:3.12-slim

WORKDIR /app

# System deps (καθαρό build, χωρίς cache bloat)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Το Render (ή όποιο host) περνάει PORT env var· ο Flask keep-alive το διαβάζει.
ENV PORT=1000
EXPOSE 1000

CMD ["python", "main.py"]
