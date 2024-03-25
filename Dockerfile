# syntax = docker/dockerfile:1.4
FROM python:3.10 AS compile-stage
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
    pip install -U pip setuptools wheel pip-tools && \
    pip install \
      -r requirements/main.txt \
      -r requirements/dev.txt \
      -r requirements/production.txt && \
    pip install aws

FROM compile-stage AS tests-stage

USER nobody