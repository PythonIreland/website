# syntax=docker/dockerfile:1.19.0
FROM python:3.13 AS compile-stage
RUN --mount=type=cache,target=/var/cache/apt \
    apt update && \
    apt install -y --no-install-recommends \
        build-essential gcc neovim fish less iputils-ping postgresql-client \
        ack
ADD requirements/main.txt \
    requirements/dev.txt \
    requirements/production.txt \
    ./requirements/
RUN --mount=type=cache,target=/root/.cache \
    pip install -U pip uv ruff && \
    python -m uv pip install \
      -r requirements/main.txt \
      -r requirements/dev.txt \
      -r requirements/production.txt aws

FROM compile-stage AS tests-stage

