from typing import Any
from rest_framework import serializers
from .models import JobsModel
from core.translationsmixin import TranslationsSerializerMixin


class JobsModelBaseSerializer(TranslationsSerializerMixin, serializers.ModelSerializer):
        class Meta:
            model = JobsModel
            fields = '__all__'

class JobsModelApiSerializer(JobsModelBaseSerializer):  
    class Meta(JobsModelBaseSerializer.Meta):
        fields = ['id', 'title', 'description'] 
