# Fixed Dockerfile with compatible LangChain versions
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to latest version
RUN pip install --upgrade pip

# Install Python dependencies with compatible versions
RUN pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn[standard]==0.24.0 \
    gunicorn==21.2.0 \
    sqlalchemy==2.0.25 \
    pydantic==2.5.2 \
    pydantic-settings==2.1.0 \
    python-multipart==0.0.6 \
    python-dotenv==1.0.0 \
    requests==2.31.0 \
    feedparser==6.0.10 \
    beautifulsoup4==4.12.2 \
    lxml==4.9.4 \
    openai==1.10.0 \
    langchain==0.1.0 \
    langchain-openai==0.0.5 \
    langchain-community==0.0.10 \
    redis==5.0.1

# Copy application code
COPY . .

# Create non-root user and set permissions
RUN groupadd -r appuser && useradd -r -g appuser appuser \
    && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Production command
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]