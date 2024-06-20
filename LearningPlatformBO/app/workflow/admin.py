from modeltranslation.admin import TabbedTranslationAdmin
from workflow import models
from django.contrib import admin
from core.admin import admin_site


@admin.register(models.TestModel, site=admin_site)
class TestModelAdmin(TabbedTranslationAdmin, admin.ModelAdmin):
    list_display = ("id", "name")

