# BUILD
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder


ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# RUNTIME
FROM python:3.12-slim-bookworm AS runtime

RUN groupadd --system --gid 999 no-root \
    && useradd --system --gid 999 --uid 999 --create-home no-root

WORKDIR /app

COPY --from=builder --chown=no-root:no-root /app /app

ENV PATH="/app/.venv/bin:$PATH"

USER no-root

EXPOSE 8000

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "src", "--reload-delay", "3"]