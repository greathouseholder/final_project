FROM python:3.11-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-cache

COPY src ./src
#COPY data ./data
COPY scripts ./scripts
COPY main.py .

RUN mkdir -p /src/shared/logs

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]