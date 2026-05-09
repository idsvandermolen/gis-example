from pathlib import Path

from django.contrib.gis.utils import LayerMapping

from .models import Municipality

mapping = {
    "name": "name",
    "geo": "MULTIPOLYGON",
}

municipalities_geojson = (
    Path(__file__).resolve().parent.parent / "data" / "municipalities_nl.geojson"
)


def run(verbose=False):
    lm = LayerMapping(Municipality, municipalities_geojson, mapping, transform=True)
    lm.save(strict=True, verbose=verbose)
