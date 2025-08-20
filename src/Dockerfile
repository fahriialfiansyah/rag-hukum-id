# syntax=docker/dockerfile:1

FROM python:3.10-slim

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# App code
COPY app.py /app/app.py
COPY data/ /app/data/
COPY pyproject.toml /app/pyproject.toml

# Create a non-root user (best practice)
RUN useradd -m appuser
RUN mkdir -p /app/chroma_db && chown -R appuser:appuser /app
USER appuser

# Streamlit default port is 8501
EXPOSE 8501

# For reproducible environment vars (may be overridden by docker-compose)
ENV PERSIST_DIR=/app/chroma_db \
    COLLECTION_NAME=bpk_hukum_id \
    GOOGLE_GENAI_MODEL=gemini-2.5-flash

# Healthcheck (simple TCP)
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]