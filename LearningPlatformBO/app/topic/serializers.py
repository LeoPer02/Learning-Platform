from rest_framework import serializers
from .models import Topic, TopicItem, Forum, Question, QuestionAttachment
from django.conf import settings

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'title', 'description']

class TopicItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicItem
        fields = '__all__'

class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = ['id', 'title', 'description']

class QuestionSerializer(serializers.ModelSerializer):
    attachments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'description', 'forum', 'created_at', 'updated_at', 'created_by', 'updated_by', 'attachments']
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

    def create(self, validated_data):
        user = self.context['request'].user if self.context['request'].user.is_authenticated else None
        validated_data['created_by'] = user
        validated_data['updated_by'] = user
        return super().create(validated_data)

class QuestionAttachmentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = QuestionAttachment
        fields = ['id', 'question', 'file', 'file_url', 'uploaded_at', 'uploaded_by']
        read_only_fields = ['uploaded_at', 'uploaded_by']

    def get_file_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.file.url) if request else obj.file.url

    def validate_file(self, file):
        # Allowed MIME types
        allowed_mime_types = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf']
        if file.content_type not in allowed_mime_types:
            raise serializers.ValidationError("Only JPEG, PNG, GIF images, and PDF files are allowed.")

        # Optionally, validate file extension as well
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf']
        ext = file.name.split('.')[-1].lower()
        if f'.{ext}' not in allowed_extensions:
            raise serializers.ValidationError("Invalid file extension. Only .jpg, .jpeg, .png, .gif, and .pdf files are allowed.")

        # Validate file size (max 5MB)
        max_file_size = 5 * 1024 * 1024  # 5MB in bytes
        if file.size > max_file_size:
            raise serializers.ValidationError("File size must be less than 5MB.")

        return file

    def create(self, validated_data):
        user = self.context['request'].user if self.context['request'].user.is_authenticated else None
        validated_data['uploaded_by'] = user
        return super().create(validated_data)
    
class QuestionDetailSerializer(serializers.ModelSerializer):
    attachments = QuestionAttachmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'created_by', 'updated_by', 'attachments']
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

class ForumDetailSerializer(serializers.ModelSerializer):
    questions = QuestionDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = Forum
        fields = ['id', 'title', 'description', 'questions']