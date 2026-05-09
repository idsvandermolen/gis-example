FROM python:3.14-trixie as base

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1 \
    DB_NAME=/tmp/db.sqlite3 \
    APP_HOME=/app

# installs 3.10, recent python-gdal require 3.12
RUN apt update \
    && apt install -y libgdal-dev sqlite3 libsqlite3-mod-spatialite \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --root-user-action=ignore --no-cache-dir uv

# application sources
COPY manage.py entrypoint.sh pyproject.toml uv.lock ./
COPY backend ./backend
COPY api ./api

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev
RUN mkdir -p -m 755 ${APP_HOME}/static

# FROM python:3.14-trixie

# # bring over the prepared app tree (including .venv)
# COPY --from=base /app /app

# WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
# CMD []
