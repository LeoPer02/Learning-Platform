from django.urls import path
from core.utilities.types import URLPatternsList
from jobs import views

app_name = "jobs"

urlpatterns: URLPatternsList = [
    path("list/", views.JobsModelList.as_view(), name="jobs-list"),
    path("get-job/<str:id>/", views.GetJobsModel.as_view(), name="get-job"),
]
