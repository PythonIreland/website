# syntax=docker/dockerfile:1.21.0

# ---- builder: install Python deps into an isolated venv via uv ----
FROM python:3.13-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.12.1 /uv /uvx /usr/local/bin/

ENV UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_PYTHON_DOWNLOADS=never \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# build-essential/gcc are only needed to build wheels that lack a prebuilt one.
# They live in this stage only and never reach the final image.
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential gcc

WORKDIR /app

COPY pyproject.toml uv.lock ./

# Install everything into a self-contained venv at /opt/venv so the final
# stage can copy it without dragging in the build toolchain.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --all-groups

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
