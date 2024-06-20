from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from .models import Course, CourseAdmin, EnrollmentRequest
from .serializers import CourseSerializer, CourseAdminSerializer, EnrollmentRequestSerializer, AdminEnrollmentRequestSerializer, CourseAdminEnrollmentRequestSerializer, EnrolledCoursesSerializer, AdminCoursesSerializer,EnrollmentRequestSerializerForEnrollment
from .permissions import IsCourseAdmin, CanCreateEnrollmentRequest
from django.db.models import Q
from django.shortcuts import get_object_or_404
import logging

# Set up logging
logger = logging.getLogger(__name__)
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [permissions.IsAuthenticated, IsCourseAdmin | permissions.IsAdminUser]
        return super(CourseViewSet, self).get_permissions()

    def get_queryset(self):
        user = self.request.user
        if self.action == 'list':
            if user.is_authenticated:
                return Course.objects.filter().distinct()
            else:
                return Course.objects.filter(visibility='public').distinct()
        return Course.objects.all()

    def retrieve(self, request, *args, **kwargs):
        course = self.get_object()
        user = request.user
        
        if user.is_authenticated:
            logger.info(f"User {user.username} (ID: {user.id}) retrieved course {course.title} (ID: {course.id})")
        else:
            logger.info(f"Anonymous user retrieved course {course.title} (ID: {course.id})")

        if course.visibility == 'public':
            return super().retrieve(request, *args, **kwargs)
        else:
            if not user.is_authenticated:
                logger.warning(f"Anonymous user denied access to course {course.title} (ID: {course.id})")
                raise PermissionDenied("You must be authenticated to access this course.")
            if not (user in course.enrolled_users.all() or CourseAdmin.objects.filter(user=user, course=course).exists()):
                logger.warning(f"User {user.username} (ID: {user.id}) denied access to course {course.title} (ID: {course.id})")
                raise PermissionDenied("You do not have permission to access this course.")
            return super().retrieve(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("You must be an admin to assign course administrators.")
        course = serializer.save()
        CourseAdmin.objects.create(user=self.request.user, course=course, is_admin=True)

class CourseAdminViewSet(viewsets.ModelViewSet):
    queryset = CourseAdmin.objects.all()
    serializer_class = CourseAdminSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


## We make it like this with an @api_view so that we only implement one type of request tt 
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, CanCreateEnrollmentRequest])
def create_enrollment_request(request):
    user = request.user
    course_id = request.data.get('course')

       # Check if the course exists
    course_exists_response = check_course_exists(course_id)
    if course_exists_response:
        return course_exists_response

    # Check for an existing enrollment request
    enrollment_exists_response = check_enrollment_request_exists(user, course_id)
    if enrollment_exists_response:
        return enrollment_exists_response

    # Proceed to create the enrollment request
    enrollment_request_data = {
        'user': user.id,
        'course': course_id,
        'status': 'pending'  # Default status
    }
    serializer = EnrollmentRequestSerializer(data=enrollment_request_data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PATCH'])
@permission_classes([IsCourseAdmin, permissions.IsAdminUser])
def update_enrollment_request(request, pk):
    logger.info(f"Received request to update enrollment request with ID: {pk}")
    logger.info(f"Request data: {request.data}")

    enrollment_request = get_object_or_404(EnrollmentRequest, pk=pk)

    # Only allow updates to certain fields, here assuming 'status'
    if 'status' in request.data:
        serializer = EnrollmentRequestSerializer(enrollment_request, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if serializer.validated_data.get('status') == 'approved':
                add_user_to_course(enrollment_request.user, enrollment_request.course)
            updated_data = serializer.data
            updated_data['updated_at'] = enrollment_request.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ')  # Add updated_at to response
            return Response(updated_data, status=status.HTTP_200_OK)
        else:
            logger.error(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    logger.error("Status field not in request data")
    return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

def add_user_to_course(user, course):
    """Function to add a user to the enrolled users of a course."""
    if user not in course.enrolled_users.all():
        course.enrolled_users.add(user)
        course.save()
        logger.info(f"Added {user.username} to {course.title}")

def check_course_exists(course_id):
    """Check if the course with the given ID exists."""
    if not Course.objects.filter(id=course_id).exists():
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
    return None

def check_enrollment_request_exists(user, course_id):
    """Check if there is an existing enrollment request for the given user and course."""
    if EnrollmentRequest.objects.filter(user=user, course_id=course_id).exists():
        return Response({'error': 'Enrollment request already exists for this course'}, status=status.HTTP_409_CONFLICT)
    return None


class ListEnrollmentRequestsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Adjust the queryset based on the user's role.
        """
        user = self.request.user
        if user.is_superuser:
            return EnrollmentRequest.objects.filter(status='pending')
        elif IsCourseAdmin().has_permission(self.request, self):
            # Assuming you have a method to check if the user is a course admin
            course_id = self.request.query_params.get('course_id')
            if not course_id:
                return EnrollmentRequest.objects.none()  # or handle error
            return EnrollmentRequest.objects.filter(course__id=course_id)
        else:
            return EnrollmentRequest.objects.none()

    def get_serializer_class(self):
        """
        Choose the serializer class based on user permissions.
        """
        user = self.request.user
        if user.is_superuser:
            return AdminEnrollmentRequestSerializer
        elif IsCourseAdmin().has_permission(self.request, self):
            return CourseAdminEnrollmentRequestSerializer
        else:
            raise permissions.PermissionDenied("You do not have permission to view this.")

    def list(self, request, *args, **kwargs):
        if not self.get_queryset():
            return Response({"error": "No data available or you do not have permission to view this."}, status=status.HTTP_403_FORBIDDEN)
        return super().list(request, *args, **kwargs)
    
class AdminCoursesView(generics.ListAPIView):
    serializer_class = AdminCoursesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view returns a list of all the courses where the current user is an admin.
        """
        user = self.request.user
        # Fetch courses where the current user is listed as an admin
        admin_courses = Course.objects.filter(courseadmin__user=user, courseadmin__is_admin=True)
        return admin_courses

class UserEnrolledCoursesView(generics.ListAPIView):
    serializer_class = EnrolledCoursesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view returns a list of all the courses where the current user is enrolled.
        """
        user = self.request.user
        return Course.objects.filter(enrolled_users=user)


class EnrolledCoursesView(generics.ListAPIView):
    serializer_class = CourseSerializer  # Assuming this serializer is adequate for both
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Course.objects.filter(
                Q(enrolled_users=user) | Q(courseadmin__user=user)
            ).distinct()
        else:
            return Course.objects.filter(visibility='public')
    
class ListCourseEnrollmentRequestsView(generics.ListAPIView):
    serializer_class = EnrollmentRequestSerializerForEnrollment  # Use the appropriate serializer
    permission_classes = [ IsCourseAdmin, permissions.IsAdminUser]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return EnrollmentRequest.objects.filter(course_id=course_id)
    
