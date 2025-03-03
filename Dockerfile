# Образ для збірки
FROM python:3.12-slim AS builder

ENV PATH "/app/scripts:${PATH}"
ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app
ADD . /app

# Встановлення залежностей проекту
COPY --from=ghcr.io/astral-sh/uv:0.5.7 /uv /uvx /bin/
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --no-install-project --no-dev

# Фінальний образ
FROM builder AS final
COPY --from=builder --chown=app:app /app /app
ENV PATH="/app/.venv/bin:$PATH"
RUN chmod +x scripts/*
