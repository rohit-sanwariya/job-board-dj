FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy

# Install curl for uv bootstrap and system deps if needed later
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Copy dependency metadata first for better caching
COPY pyproject.toml ./
# Copy lock file if you have one:
# COPY uv.lock ./

# Sync deps (creates .venv)
RUN uv sync --frozen || uv sync

# Now app code
COPY . .

# Ensure scripts are executable
RUN chmod +x entrypoint.sh

EXPOSE 8000
CMD ["./entrypoint.sh"]
