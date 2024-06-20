from workflow import views
from django.urls import path


app_name = "workflow"

urlpatterns = [
    path('test-get-view/<str:id>/', views.TestGetView.as_view(), name='test-get-view'),
    path('test-list-view/', views.TestListView.as_view(), name='test-list-view'),
    path('test-destroy-view/<str:id>/', views.TestDestroyView.as_view(), name='test-destroy-view'),
]
