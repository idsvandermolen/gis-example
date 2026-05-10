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

## Build containers
If you do not have `mise`, you can have a look at the `mise.toml` files to find the relevant commands for the mise tasks.

### Build django container
Build the container with `podman build -f Dockerfile -t gis-example:latest .` or if you use docker with `docker build -f Dockerfile -t gis-example:latest .`

### Build frontend container
Go to the `frontend` folder and build the container with `podman build -f Dockerfile -t gis-example-frontend:latest .` or if you use docker with `docker build -f Dockerfile -t gis-example-frontend:latest .`.

## Start containers
### Start the django container
Place the GeoJSON municipalities data file `municipalities_nl.geojson` into `data/` folder.
Start the container with `mise run start`, which exposes the correct ports (localhost:5173), binds the `data` directory and starts the container.

### Start the frontend container
Go to the `frontend` folder and start the container with `mise run start`, which exposes the correct ports (localhost:8000) and starts the container.

## Use
Start the containers (see above) and point your browser to http://localhost:8000 . This should provide a simple HTML page with links to these items:
* the OpenLayer frontend app
* the Swagger app to interactively use the API (CRUD operations)
* the ReDoc API documentation
* the OpenAPI API schema
* the API endpoint

## JWT Authentication
To create a superuser account, you can for example login to the container and run this command with substituted USERNAME and EMAIL address:
```shell
uv run manage.py createsuperuser --username $USERNAME --email $EMAIL
# Then enter the password (twice)
```
__NOTE__:
To enable the use of JWT authentication, the container needs to be started with the `REQUIRE_AUTHENTICATION=True` environment set (for example in the `.env` file).

We're using DRF SimpleJWT authentication (see https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html). To obtain a token use something like:
```shell
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "davidattenborough", "password": "boatymcboatface"}' \
  http://localhost:8000/token/

...
{
  "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU",
  "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"
}
```
Then use the access token to access the API:
```shell
curl \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU" \
  http://localhost:8000/api/
```

## TODO
- adjust frontend app to preserve CSRF and Authorization (JWT) headers and send them back to the API
- automatically refresh the access token with the refresh token before it expires
