# GIS example using Django and OpenLayers
This project is an example on how to use OpenLayers with a Django backend. It will show GeoJSON features on top of a map.

## Setup
Create a `.env` file from the `.env.example` file or set these environment variables explicitly:
- `DJANGO_SECRET_KEY`

Optionally set these environment variables or add them to the `.env` file:
- `DEBUG` (defaults to `False`)

## Generate django key with:
```shell
uv run python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
