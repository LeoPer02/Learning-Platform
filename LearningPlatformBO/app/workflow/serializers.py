from rest_framework import serializers
from workflow import models


class TestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TestModel
        fields = ['id', 'name']
