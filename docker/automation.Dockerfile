# Dockerfile for Playwright Automation Testing
# Runs automated test suite against the application containers

FROM python:3.11-slim

LABEL maintainer="Address Checker Team"
LABEL description="Playwright automation testing container for NZ Address Checker"

# Set working directory
WORKDIR /app

# Install system dependencies for Playwright and browsers
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY tests/requirements.txt /app/tests/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/tests/requirements.txt

# Install Playwright browsers
RUN python -m playwright install chromium

# Copy test files
COPY tests /app/tests
COPY backend /app/backend
COPY frontend /app/frontend

# Set environment variables for headless testing in container
ENV HEADLESS=true
ENV SLOW_MO=0
ENV TIMEOUT=30000
ENV BASE_URL=http://address-checker-frontend
ENV BACKEND_URL=http://address-checker-api:8000

# Create screenshots directory
RUN mkdir -p /app/tests/screenshots /app/test-results

# Health check to ensure app is accessible
HEALTHCHECK --interval=5s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f ${BACKEND_URL}/health || exit 1

# Run pytest with verbose output and HTML report
CMD ["sh", "-c", "pytest tests/smoke tests/sanity -v --tb=short --html=/app/test-results/report.html --self-contained-html"]
