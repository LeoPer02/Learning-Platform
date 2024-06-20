from django.db import models
from core.extensions.models.base_abstract_model import BaseAbstractModel 

#The BaseAbstractModel brings a uuid, created_at, updated_at and deleted_at
class JobsModel(BaseAbstractModel):

    title = models.CharField(max_length=255)
    description = models.TextField()
    is_visible = models.BooleanField(
        default=False, help_text="Designates this object as being visible", verbose_name="visibility status"
    )

    auto_translate_fields = ("title","description")

    class Meta:
        verbose_name_plural = "Job Details"
        ordering = ['created_at']

    # This is used by the admin
    def __str__(self):
        return f"Title: {self.title}, Description: {self.description}, Is visible: {self.is_visible} "
