from rest_framework import viewsets, permissions,status
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Topic, TopicItem, Forum, Question, QuestionAttachment
from .serializers import TopicSerializer, TopicItemSerializer, ForumSerializer, QuestionSerializer, QuestionAttachmentSerializer, ForumDetailSerializer
from .permissions import IsOwnerOrReadOnly
from course.models import CourseAdmin
from django.db import transaction

class IsCourseAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        course = obj.course
        return CourseAdmin.objects.filter(user=request.user, course=course).exists()

class IsEnrolledOrCourseAdminOrPublic(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the related course is public
        if obj.question.forum.course.visibility == 'public':
            return True
        
        # If the course is private, check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Check if the user is enrolled, a course admin, or a superuser
        course = obj.question.forum.course
        return (course.enrolled_users.filter(id=request.user.id).exists() or
                CourseAdmin.objects.filter(user=request.user, course=course).exists() or
                request.user.is_superuser)
    
class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            return [IsCourseAdmin()]
        return [IsOwnerOrReadOnly()]

    def create(self, request, *args, **kwargs):
        course_id = request.data.get('course')
        if not CourseAdmin.objects.filter(user=request.user, course_id=course_id).exists():
            raise PermissionDenied("You do not have permission to create a topic in this course.")
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(course_id=course_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the user is a course admin
        course = instance.course
        if not CourseAdmin.objects.filter(user=request.user, course=course).exists():
            raise PermissionDenied("You do not have permission to edit this topic.")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the user is a course admin
        course = instance.course
        if not CourseAdmin.objects.filter(user=request.user, course=course).exists():
            raise PermissionDenied("You do not have permission to edit this topic.")
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        course = instance.course
        if not CourseAdmin.objects.filter(user=request.user, course=course).exists():
            raise PermissionDenied("You do not have permission to delete this topic.")
        return super().destroy(request, *args, **kwargs)

class TopicItemViewSet(viewsets.ModelViewSet):
    queryset = TopicItem.objects.all()
    serializer_class = TopicItemSerializer
    permission_classes = [IsOwnerOrReadOnly]

class ForumViewSet(viewsets.ModelViewSet):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            permission_classes = [IsCourseAdmin]
        elif self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        course_id = request.data.get('course')
        if not CourseAdmin.objects.filter(user=request.user, course_id=course_id).exists():
            raise PermissionDenied("You do not have permission to create a forum in this course.")
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(course_id=course_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the user is a course admin
        course = instance.course
        if not CourseAdmin.objects.filter(user=request.user, course=course).exists():
            raise PermissionDenied("You do not have permission to edit this forum.")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the user is a course admin
        course = instance.course
        if not CourseAdmin.objects.filter(user=request.user, course=course).exists():
            raise PermissionDenied("You do not have permission to edit this forum.")
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        course = instance.course
        if not CourseAdmin.objects.filter(user=request.user, course=course).exists():
            raise PermissionDenied("You do not have permission to delete this forum.")
        return super().destroy(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ForumDetailSerializer(instance)
        return Response(serializer.data)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.action == 'create':
            forum_id = self.request.data.get('forum')
            if forum_id:
                try:
                    forum = Forum.objects.get(id=forum_id)
                    if forum.course.visibility == 'public':
                        return [permissions.AllowAny()]
                except Forum.DoesNotExist:
                    raise PermissionDenied("The forum does not exist.")
            return [IsCourseAdmin]
        else:
            return [permissions.IsAuthenticated()]
        
    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(created_by=user, updated_by=user)

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = request.user if request.user.is_authenticated else None
            question = serializer.save(created_by=user, updated_by=user)

            file = request.FILES.get('file')
            if file:
                attachment_data = {
                    'question': question.id,
                    'file': file
                }
                attachment_serializer = QuestionAttachmentSerializer(data=attachment_data, context={'request': request})
                if attachment_serializer.is_valid():
                    attachment_serializer.save(uploaded_by=user)
                else:
                    question.delete()
                    return Response(attachment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
class QuestionAttachmentViewSet(viewsets.ModelViewSet):
    queryset = QuestionAttachment.objects.all()
    serializer_class = QuestionAttachmentSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return [IsEnrolledOrCourseAdminOrPublic()]
        return [permissions.IsAuthenticated()]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        file_handle = instance.file.open()
        response = FileResponse(file_handle, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{instance.file.name.split("/")[-1]}"'
        return response
