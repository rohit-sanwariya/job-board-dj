FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    PATH="/root/.local/bin:${PATH}"

# Install curl for uv bootstrap + system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gcc libpq-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv (Python package/dependency manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /app

# Copy dependency metadata first (better caching)
COPY pyproject.toml ./
# If you have uv.lock, copy that too
# COPY uv.lock ./

# Install dependencies into container (creates .venv inside /app/.venv)
RUN uv sync --frozen || uv sync

# Copy the rest of the project
COPY . .

# Make sure entrypoint is executable
RUN chmod +x entrypoint.sh

# Expose Django port
EXPOSE 8000

# Run entrypoint (which can run migrations, collectstatic, etc.)
CMD ["./entrypoint.sh"]
