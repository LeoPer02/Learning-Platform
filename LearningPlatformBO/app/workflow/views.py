from drf_spectacular.utils import extend_schema
from rest_framework import generics
from workflow import models
from workflow import serializers 


@extend_schema(tags=["Test Endpoints"])
class TestGetView(generics.RetrieveAPIView):
    """Test get view description"""
    lookup_field = "id"
    queryset = models.TestModel.objects.all()
    serializer_class = serializers.TestModelSerializer


@extend_schema(tags=["Test Endpoints"])
class TestListView(generics.ListAPIView):
    """Test list view description"""

    queryset = models.TestModel.objects.all()
    serializer_class = serializers.TestModelSerializer


@extend_schema(tags=["Test Endpoints"])
class TestDestroyView(generics.DestroyAPIView):
    """Test destroy view description"""
    lookup_field = "id"
    queryset = models.TestModel.objects.all()

