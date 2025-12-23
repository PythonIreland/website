# syntax=docker/dockerfile:1.19.0
FROM python:3.13 AS compile-stage
RUN --mount=type=cache,target=/var/cache/apt \
    apt update && \
    apt install -y --no-install-recommends \
        build-essential gcc neovim fish less iputils-ping postgresql-client \
        ack

# Copy dependency specification files
COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache \
    pip install -U pip uv ruff && \
    uv sync --group production

FROM compile-stage AS tests-stage

