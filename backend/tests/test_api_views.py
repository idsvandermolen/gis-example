import pytest
from django.contrib.gis.geos import MultiPolygon, Polygon
from django.urls import reverse
from rest_framework import status

from api.models import Municipality


@pytest.mark.django_db
class TestMunicipalityViews:
    def test_municipality_list(self, api_client):
        # Create a test municipality
        poly = MultiPolygon(Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))))
        Municipality.objects.create(name="Test City", geo=poly)

        url = reverse("api:municipality-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        # Verify GeoJSON format provided by GeoJsonPagination
        assert response.data["type"] == "FeatureCollection"
        assert "features" in response.data
        assert len(response.data["features"]) == 1
        assert response.data["features"][0]["properties"]["name"] == "Test City"

    def test_municipality_bbox_filter(self, api_client):
        # Create two municipalities in different locations
        poly1 = MultiPolygon(Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))))
        Municipality.objects.create(name="City A", geo=poly1)

        poly2 = MultiPolygon(
            Polygon(((10, 10), (10, 11), (11, 11), (11, 10), (10, 10)))
        )
        Municipality.objects.create(name="City B", geo=poly2)

        url = reverse("api:municipality-list")

        # 1. Filter for City A using a bounding box that contains it
        response = api_client.get(url, {"in_bbox": "-0.5,-0.5,1.5,1.5"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["features"]) == 1
        assert response.data["features"][0]["properties"]["name"] == "City A"

        # 2. Filter for City B
        response = api_client.get(url, {"in_bbox": "9.5,9.5,11.5,11.5"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["features"]) == 1
        assert response.data["features"][0]["properties"]["name"] == "City B"

        # 3. Filter for an empty area
        response = api_client.get(url, {"in_bbox": "5,5,6,6"})
        assert len(response.data["features"]) == 0

    def test_municipality_detail(self, api_client):
        poly = MultiPolygon(Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))))
        municipality = Municipality.objects.create(name="Detail City", geo=poly)
        url = reverse("api:municipality-detail", kwargs={"pk": municipality.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["properties"]["name"] == "Detail City"

    def test_municipality_create(self, api_client):
        url = reverse("api:municipality-list")
        data = {
            "name": "New City",
            "geo": {
                "type": "MultiPolygon",
                "coordinates": [[[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]],
            },
        }
        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Municipality.objects.filter(name="New City").exists()

    def test_municipality_update(self, api_client):
        poly = MultiPolygon(Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))))
        municipality = Municipality.objects.create(name="Old City", geo=poly)
        url = reverse("api:municipality-detail", kwargs={"pk": municipality.pk})
        data = {
            "name": "Updated City",
            "geo": {
                "type": "MultiPolygon",
                "coordinates": [[[[1, 1], [1, 2], [2, 2], [2, 1], [1, 1]]]],
            },
        }
        response = api_client.put(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        municipality.refresh_from_db()
        assert municipality.name == "Updated City"

    def test_municipality_partial_update(self, api_client):
        poly = MultiPolygon(Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))))
        municipality = Municipality.objects.create(name="Partial City", geo=poly)
        url = reverse("api:municipality-detail", kwargs={"pk": municipality.pk})
        data = {"name": "Patched City"}
        response = api_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        municipality.refresh_from_db()
        assert municipality.name == "Patched City"

    def test_municipality_delete(self, api_client):
        poly = MultiPolygon(Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))))
        municipality = Municipality.objects.create(name="Delete City", geo=poly)
        url = reverse("api:municipality-detail", kwargs={"pk": municipality.pk})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Municipality.objects.filter(pk=municipality.pk).exists()
