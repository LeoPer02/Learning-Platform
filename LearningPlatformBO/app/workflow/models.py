from django.db import models
from core.extensions.models.base_abstract_model import BaseAbstractModel
from workflow.model_mixins import AutoTranslateableModelMixin


class TestModel(AutoTranslateableModelMixin, BaseAbstractModel):
    name = models.CharField(max_length=255)

    auto_translate_fields = ("title",)

    def __str__(self):
        return f"Name: {self.name}"


