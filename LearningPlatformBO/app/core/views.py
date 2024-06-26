from typing import Any
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView


@extend_schema(tags=["Core"])
@extend_schema(responses={status.HTTP_200_OK: {"type": "string", "enum": ["pong"]}})
class PingView(APIView):
    """View that simply replies with a 'pong'."""

    http_method_names = ["get"]

    def get(self, *args: Any, **kwargs: Any) -> Response:
        return Response("pong", status=status.HTTP_200_OK)
