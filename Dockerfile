# Multi-stage Dockerfile for Mini Insurance Document Validator
# Uses Python 3.12 and uv for fast dependency management

# Stage 1: Builder stage
FROM python:3.12-slim AS builder

WORKDIR /app

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set environment variables for Python and uv
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv to system Python (no venv)
RUN uv sync --frozen --no-dev

# Stage 2: Runtime stage
FROM python:3.12-slim

WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    PORT=8000

# Copy Python dependencies from builder stage (virtual environment)
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY main.py .
COPY models.py .
COPY ai_extractor.py .
COPY validation.py .

# Copy required assets
COPY provided_assets/ ./provided_assets/

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose the port
EXPOSE 8000

# Command to run the application
# Uses shell form to allow environment variable substitution for $PORT
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
