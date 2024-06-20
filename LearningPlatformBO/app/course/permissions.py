from rest_framework import permissions
from .models import Course, CourseAdmin, EnrollmentRequest

class IsCourseAdmin(permissions.BasePermission):
    """Custom permission to only allow admins of a course to edit or delete it."""
    def has_object_permission(self, request, view, obj):
        return CourseAdmin.objects.filter(user=request.user, course=obj).exists()
        #, is_admin=True Add this when I create new database TODO
     
class CanCreateEnrollmentRequest(permissions.BasePermission):
    message = "You are not allowed to enroll in this course."

    def has_permission(self, request, view):
        course_id = request.data.get('course')
        user = request.user
        if not course_id:
            return False

        # Check if user is already enrolled or has a pending/approved request
        if EnrollmentRequest.objects.filter(user=user, course_id=course_id).exists():
            return False
        return True