FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    make \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /workspaces/seek-core

# Install development tools
RUN pip install --no-cache-dir black flake8 pytest pytest-cov mypy isort

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# The actual dependencies will be installed by postCreateCommand in devcontainer.json
