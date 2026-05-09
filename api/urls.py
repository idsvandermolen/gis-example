from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MunicipalityViewSet

app_name = "api"

router = DefaultRouter()
router.register(r"", MunicipalityViewSet, basename="municipality")
urlpatterns = [
    path("", include(router.urls)),
]
