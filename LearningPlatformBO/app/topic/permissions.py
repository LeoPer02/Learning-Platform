from rest_framework import permissions
from course.models import CourseAdmin

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner
        if obj.created_by == request.user:
            return True
        # Check if the user is a course admin
        course = obj.course
        if CourseAdmin.objects.filter(user=request.user, course=course).exists():
            return True
        return False