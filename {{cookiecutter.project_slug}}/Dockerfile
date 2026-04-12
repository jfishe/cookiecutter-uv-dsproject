# ---------------------------------------------------------------------------
# Multi-stage uv build
# ---------------------------------------------------------------------------
FROM ghcr.io/astral-sh/uv:python{{ cookiecutter.python_version }}-bookworm-slim AS builder

WORKDIR /app

# Install dependencies first (layer cache)
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy source & install project
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ---------------------------------------------------------------------------
# Runtime
# ---------------------------------------------------------------------------
FROM python:{{ cookiecutter.python_version }}-slim-bookworm AS runtime

RUN groupadd --gid 1000 app && \
    useradd  --uid 1000 --gid app --create-home app

COPY --from=builder --chown=app:app /app /app
WORKDIR /app

USER app
ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["python", "-m", "{{ cookiecutter.package_name }}"]
