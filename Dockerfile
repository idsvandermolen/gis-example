FROM python:3.14-trixie as base

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    DB_NAME=/tmp/db.sqlite3 \
    APP_HOME=/app

# installs 3.10, recent python-gdal require 3.12
RUN apt update \
    && apt install -y libgdal-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --root-user-action=ignore --no-cache-dir uv

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock,relabel=shared,rw \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml,relabel=shared \
    uv sync --locked --no-install-project --no-dev

RUN mkdir -p -m 755 ${APP_HOME}/static

# application sources
COPY manage.py entrypoint.sh ./
COPY backend ./backend

# FROM python:3.14-trixie

# # bring over the prepared app tree (including .venv)
# COPY --from=base /app /app

# WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
# CMD []
