from django.db import connections
from drf_spectacular.utils import OpenApiExample, extend_schema, inline_serializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import BooleanField


@extend_schema(
    operation_id="api_alive",
    responses=inline_serializer(name="alive", fields={"alive": BooleanField()}),
)
@api_view(["GET"])
@permission_classes([AllowAny])
def alive(request):
    "Check if API is alive."
    return Response({"alive": True}, status=status.HTTP_200_OK)


@extend_schema(
    operation_id="api_ready",
    responses={
        200: inline_serializer(name="ready", fields={"ready": BooleanField()}),
        503: inline_serializer(name="notready", fields={"ready": BooleanField()}),
    },
    examples=[
        OpenApiExample(
            name="ready",
            response_only=True,
            value={"ready": True},
            status_codes=["200"],
        ),
        OpenApiExample(
            name="notready",
            response_only=True,
            value={"ready": False},
            status_codes=["503"],
        ),
    ],
)
@api_view(["GET"])
@permission_classes([AllowAny])
def ready(request):
    "Check if API is ready to accept traffic."
    if connections["default"].is_usable():
        return Response({"ready": True}, status=status.HTTP_200_OK)
    return Response({"ready": False}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
