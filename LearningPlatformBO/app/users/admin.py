import django.contrib.auth.models as admin_models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.admin import admin_site
from users import models


@admin.register(models.User, site=admin_site)
class UserAdmin(BaseUserAdmin):
    list_display = (models.User.USERNAME_FIELD, "id", "is_active", "is_staff")
    search_fields = (models.User.USERNAME_FIELD,)
    ordering = ("created_at",)

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (models.User.USERNAME_FIELD, "password1", "password2"),
            },
        ),
    )

    readonly_fields = ("id", "created_at", "updated_at", "last_login")
    fieldsets = (
        ("Object details", {"fields": ("id", models.User.USERNAME_FIELD, "is_active", "is_deleted", "password")}),
        ("Datetime information", {"fields": ("created_at", "updated_at", "last_login")}),
        ("Permissions", {"fields": ("is_superuser", "is_staff", "groups", "user_permissions")}),
    )


# Register the default Group and Permissions models.
# This next code block is a workaround to place them under the "Users" label
# See https://stackoverflow.com/questions/10561091/ for more details
class GroupProxy(admin_models.Group):
    class Meta:
        proxy = True
        verbose_name = "group"


@admin.register(GroupProxy, site=admin_site)
class GroupAdmin(admin.ModelAdmin):
    fields = ("name", "permissions")
    filter_horizontal = ("permissions",)


class PermissionProxy(admin_models.Permission):
    class Meta:
        proxy = True
        verbose_name = "permission"


admin_site.register(PermissionProxy)
