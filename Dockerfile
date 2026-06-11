# syntax=docker/dockerfile:1.21.0

# ---- builder: compile and install Python deps into an isolated venv ----
FROM python:3.13-slim AS builder

ENV UV_LINK_MODE=copy \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# build-essential/gcc are only needed to build wheels that lack a prebuilt one.
# They live in this stage only and never reach the final image.
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential gcc

RUN --mount=type=cache,target=/root/.cache \
    pip install -U pip uv

COPY requirements/main.txt \
     requirements/dev.txt \
     requirements/production.txt \
     ./requirements/

# Install everything into a self-contained venv at /opt/venv so the final
# stage can copy it without dragging in the build toolchain.
RUN --mount=type=cache,target=/root/.cache \
    uv venv /opt/venv && \
    uv pip install --python /opt/venv \
      -r requirements/main.txt \
      -r requirements/dev.txt \
      -r requirements/production.txt

# ---- dev: lean runtime image with interactive tooling (used by web + test) ----
FROM python:3.13-slim AS dev

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Runtime-only system packages: the postgres client for psql/pg_dump plus the
# interactive tooling the dev shell relies on (compose runs `fish`).
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        postgresql-client \
        fish neovim less ack iputils-ping

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app
