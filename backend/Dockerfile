FROM python:3.14-trixie as base

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1 \
    APP_HOME=/app \
    DB_NAME=/app/data/db.sqlite3

# installs 3.10, recent python-gdal require 3.12
RUN apt update \
    && apt install -y libgdal-dev sqlite3 libsqlite3-mod-spatialite \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --root-user-action=ignore --no-cache-dir uv \
    && mkdir -p -m 755 ${APP_HOME}/static

# Copy uv stuff (from backend folder when building from repo root)
COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev

# application sources
COPY manage.py entrypoint.sh ./
COPY backend ./backend
COPY api ./api
COPY etc ./etc

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
