from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestBackendViews:
    def test_alive_view(self, api_client):
        url = reverse("alive")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"alive": True}

    def test_ready_view_success(self, api_client):
        url = reverse("ready")
        # By default, the test database connection is usable
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"ready": True}

    def test_ready_view_failure(self, api_client):
        url = reverse("ready")
        # Patch the database connections used in the view to simulate failure
        with patch("backend.views.connections") as mock_connections:
            mock_connections.__getitem__.return_value.is_usable.return_value = False
            response = api_client.get(url)
            assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
            assert response.data == {"ready": False}
