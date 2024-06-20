from rest_framework import serializers
from .models import Course, CourseAdmin, EnrollmentRequest
from topic.serializers import TopicSerializer, ForumSerializer
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

class CourseSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    forums = ForumSerializer(many=True, read_only=True)
    enrolled_users = serializers.PrimaryKeyRelatedField(
        many=True,
        required=False,
        allow_empty=True,  # Allows the list to be empty
        read_only=True     # Ensures the field is read-only
    )
    is_course_admin = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
    
    def get_is_course_admin(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return CourseAdmin.has_course_admin_permission(request.user, obj)
        return False
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            if CourseAdmin.has_course_admin_permission(request.user, instance):
                representation['isAdmin'] = True
        return representation

class CourseAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseAdmin
        fields = ['id', 'user', 'course', 'is_admin']

class EnrollmentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentRequest
        fields = ['id', 'user', 'course', 'status']
        read_only_fields = ('user','id')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        validated_data['status'] = 'pending'
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
    
class AdminEnrollmentRequestSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField()  # Add a custom method field for course name

    class Meta:
        model = EnrollmentRequest
        fields = ['course_id', 'course_name', 'user_id']

    def get_course_name(self, obj):
        # This method will be used to fetch the course name
        return obj.course.title if obj.course else None

class CourseAdminEnrollmentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentRequest
        fields = ['user_id']

class EnrolledCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'visibility', 'topics', 'created_at', 'updated_at']

class AdminCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'visibility', 'topics', 'created_at', 'updated_at']

class UserSerializerForEnrollment(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email'] 

class EnrollmentRequestSerializerForEnrollment(serializers.ModelSerializer):
    user = UserSerializerForEnrollment()

    class Meta:
        model = EnrollmentRequest
        fields = ['id', 'user', 'course', 'status', 'created_at', 'updated_at']