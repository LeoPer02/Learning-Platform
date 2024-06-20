from django.contrib import admin
from core.admin import admin_site
from course import models

@admin.register(models.Course, site=admin_site)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "visibility")

    readonly_fields = ("id", "created_at", "updated_at")

    fieldsets = (
        (models.Course._meta.verbose_name_plural, {"fields": ("id", "visibility", "title")}),
    )