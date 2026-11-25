FROM python:3.15-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY src/ ./src/
COPY alembic.ini ./
COPY migrations/ ./migrations/

CMD ["/app/.venv/bin/fastapi", "run", "src/main.py", "--host", "0.0.0.0", "--port", "8000"]
