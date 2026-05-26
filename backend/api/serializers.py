from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Municipality


class MunicipalitySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Municipality
        geo_field = "geo"
        fields = ["id", "name"]
