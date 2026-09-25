# syntax=docker/dockerfile:1.21.0
FROM python:3.13 AS compile-stage
RUN --mount=type=cache,target=/var/cache/apt \
    apt update && \
    apt install -y --no-install-recommends \
        build-essential gcc neovim fish less iputils-ping postgresql-client \
        ack
ADD pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache \
    pip install -U pip uv && \
    uv sync --frozen --all-groups
ENV PATH="/.venv/bin:$PATH"

FROM compile-stage AS tests-stage

