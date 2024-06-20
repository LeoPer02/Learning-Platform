from typing import Any
from rest_framework import serializers
from users import models
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from course.models import CourseAdmin

class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for creating users."""

    class Meta:
        model = models.User
        extra_kwargs = {"password": {"write_only": True}}
        # Because more fields can be included in the user, instead exclude all that we know we don't want
        # Exception: do not exclude password
        exclude = (
            "id",
            "created_at",
            "updated_at",
            "is_deleted",
            "is_staff",
            "is_active",
            "is_superuser",
            "last_login",
            "groups",
            "user_permissions",
        )

    def create(self, validated_data: Any) -> models.User:
        return models.User.objects.create_user(**validated_data)

class PublicUserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for public user registration."""

    class Meta:
        model = models.User
        extra_kwargs = {"password": {"write_only": True}}
        fields = ['username', 'password', 'email']  # Customize based on public registration needs

    def create(self, validated_data):
        """Create a new user."""
        user = models.User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    def to_representation(self, instance):
        """Modify the output that the serializer provides, adding tokens."""
        user_repr = super().to_representation(instance)  # Get the default serialization.
        refresh = RefreshToken.for_user(instance)
        user_repr['tokens'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return user_repr
    
class UserWhoamiSerializer(serializers.ModelSerializer):
    """Serializer for retrieving the current user's `USERNAME_FIELD` data (usually username or email)."""

    class Meta:
        model = models.User
        fields = (models.User.USERNAME_FIELD,)


class UserChangePasswordSerializer(serializers.ModelSerializer):
    """Serializer for change password requests."""

    new_password = serializers.CharField(required=True)

    class Meta:
        model = models.User
        fields = ("new_password", )


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer to handle user's details."""

    class Meta:
        model = models.User
        # Because more fields can be included in the user, instead exclude all that we know we don't want
        exclude = (
            "id",
            "created_at",
            "updated_at",
            "is_deleted",
            "is_active",
            "is_superuser",
            "password",
            "last_login",
            "groups",
            "user_permissions",
        )

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_admin'] = user.is_staff

        courses_admin = CourseAdmin.objects.filter(user=user).values_list('course_id', flat=True)
        token['courses_admin'] = list(courses_admin)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        return data