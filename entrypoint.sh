#!/bin/bash
set -euo pipefail
uv run ./manage.py check
uv run ./manage.py collectstatic --noinput
uv run ./manage.py migrate --noinput
uv run manage.py shell -c 'from api.load import run;run()'
uv run gunicorn --config etc/gunicorn.conf.py
