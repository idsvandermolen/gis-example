#!/bin/bash
set -euo pipefail
uv run ./manage.py check
uv run ./manage.py collectstatic --noinput
uv run ./manage.py migrate --noinput
# Allow passing an optional path as the first arg; fall back to bundled file
DATA_FILE=${1:-data/municipalities_nl.geojson}
export DATA_FILE
uv run ./manage.py shell -c "from api.load import run; run()"
uv run gunicorn --config etc/gunicorn.conf.py
