# Flask fake-news-detector container
FROM python:3.10-slim

WORKDIR /app

# Install system deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Expose Flask port
ENV PORT=8080
EXPOSE 8080

# Default command
CMD ["python", "app.py"]
