FROM astral/uv:python3.13-bookworm

WORKDIR /app

# Copy pyproject.toml for dependency management
COPY pyproject.toml .

# Create a virtual environment and install dependencies
RUN uv venv
RUN uv sync

ENV PYTHONUNBUFFERED=1

