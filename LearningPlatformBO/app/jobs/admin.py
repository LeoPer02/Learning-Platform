from django.contrib import admin
from core.admin import admin_site
from jobs import models
from .models import JobsModel
from modeltranslation.admin import TabbedTranslationAdmin

@admin.register(models.JobsModel, site=admin_site)
class JobsModelAdmin(TabbedTranslationAdmin, admin.ModelAdmin):
    list_display = ("id", "title", "is_visible")

    readonly_fields = ("id", "created_at", "updated_at")

    fieldsets = (
        (JobsModel._meta.verbose_name_plural, {"fields": ("id", "is_visible", "title", "description", "is_deleted",)}),
    )