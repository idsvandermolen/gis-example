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

# Build and run containers
If you do not have `mise`, you can have a look at the `mise.toml` files to find the relevant commands for the mise tasks.

## Build django container
Build the container with `podman build -f Dockerfile -t gis-example:latest .` or if you use docker with `docker build -f Dockerfile -t gis-example:latest .`

## Start the django container
Place the GeoJSON municipalities data file `municipalities_nl.geojson` into `data/` folder.
Start the container with `mise run start`, which exposes the correct ports, binds the `data` directory and starts the container.

## Build frontend container
Go to the `frontend` folder and build the container with `podman build -f Dockerfile -t gis-example-frontend:latest .` or if you use docker with `docker build -f Dockerfile -t gis-example-frontend:latest .`.

## Start the frontend container
Go to the `frontend` folder and start the container with `mise run start`, which exposes the correct ports and starts the container.
