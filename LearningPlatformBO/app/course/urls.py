from django.urls import path, include
from .views import CourseViewSet, CourseAdminViewSet, create_enrollment_request, update_enrollment_request, ListEnrollmentRequestsView, EnrolledCoursesView,ListCourseEnrollmentRequestsView
from core.utilities.types import URLPatternsList

urlpatterns: URLPatternsList = [
    path('courses/', CourseViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='course-list'),
    path('courses/<int:pk>/', CourseViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='course-detail'),
    path('courseadmins/', CourseAdminViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='courseadmin-list'),
    path('courseadmins/<int:pk>/', CourseAdminViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='courseadmin-detail'),
    path('enrollment-requests-list/', ListEnrollmentRequestsView.as_view(), name='list-enrollment-requests'),
    path('enrollment-requests/', create_enrollment_request, name='create-enrollment-request'),
    path('enrollment-requests/<int:pk>/', update_enrollment_request, name='update-enrollment-request'),
    path('enrolled-courses/', EnrolledCoursesView.as_view(), name='enrolled-courses'),
    path('courses/<int:course_id>/enrollment-requests/', ListCourseEnrollmentRequestsView.as_view(), name='course-enrollment-requests'),
]