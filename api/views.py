from django.http import HttpResponse
from django.template import loader
from rest_framework.viewsets import ModelViewSet
from rest_framework_gis.filters import InBBOXFilter

from .models import Municipality
from .serializers import MunicipalitySerializer


def index(request):
    template = loader.get_template("api/index.html")
    context = {}
    return HttpResponse(template.render(context, request))


class MunicipalityViewSet(ModelViewSet):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer
    bbox_filter_field = "geo"
    filter_backends = (InBBOXFilter,)
