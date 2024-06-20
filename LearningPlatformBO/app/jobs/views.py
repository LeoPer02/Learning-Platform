from drf_spectacular.utils import extend_schema
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from jobs import serializers, models


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100
           
class VisibleJobsAPIView(generics.GenericAPIView):
    """Base view for Job models that are visible."""
    queryset = models.JobsModel.objects.all()

    def get_queryset(self):
        """
        Override to return only visible jobs.
        """
        return super().get_queryset().filter(is_visible=True)
    
@extend_schema(tags=["Jobs Endpoints"])
class JobsModelList(VisibleJobsAPIView, generics.ListAPIView):
    """ This returns all the jobs """
    serializer_class = serializers.JobsModelApiSerializer
    pagination_class = StandardResultsSetPagination

@extend_schema(tags=["Jobs Endpoints"])
class GetJobsModel(VisibleJobsAPIView, generics.RetrieveAPIView):
    """Get view description"""
    lookup_field = "id"
    serializer_class = serializers.JobsModelApiSerializer


"""
If we want to do an endpoint to delete we can use generics.DestroyAPIView
"""