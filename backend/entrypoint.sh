#!/bin/bash
set -euo pipefail
IMPORT_DATA=$(test -f $DB_NAME; echo $?)
uv run ./manage.py check
uv run ./manage.py collectstatic --noinput
uv run ./manage.py migrate --noinput
if [ "$IMPORT_DATA" = "1" ]; then
    # Allow passing an optional path as the first arg; fall back to bundled file
    export DATA_FILE=${1:-/app/data/municipalities_nl.geojson}
    uv run ./manage.py shell -c "from api.load import run; run()"
fi
uv run gunicorn --config etc/gunicorn.conf.py
