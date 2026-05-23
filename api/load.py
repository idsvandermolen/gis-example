from pathlib import Path
import os

from django.contrib.gis.utils import LayerMapping

from .models import Municipality

mapping = {
    "name": "name",
    "geo": "MULTIPOLYGON",
}

def run(data_file=None, verbose=False):
    """Load municipalities from a GeoJSON file.

    `data_file` may be provided directly. If it's not provided the
    function will read the `DATA_FILE` environment variable. If that
    environment variable is missing the function raises a RuntimeError.
    """
    if data_file is None:
        data_file = os.environ.get('DATA_FILE')
        if not data_file:
            raise RuntimeError('DATA_FILE environment variable is not set')

    data_path = Path(data_file)

    lm = LayerMapping(Municipality, data_path, mapping, transform=True)
    lm.save(strict=True, verbose=verbose)
