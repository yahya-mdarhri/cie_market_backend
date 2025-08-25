from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Notification, ActivityLog


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("email", "is_staff", "is_superuser", "is_active", "inventor")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("email",)
    ordering = ("email",)

    # Fields shown when editing/creating user
    fieldsets = (
        (None, {"fields": ("email", "password", "inventor")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_superuser", "is_active"),
        }),
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("user__email", "message")
    ordering = ("-created_at",)


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("user", "action", "activity_type", "created_at")
    list_filter = ("activity_type", "created_at")
    search_fields = ("user__email", "action")
    ordering = ("-created_at",)


# Register custom User model
admin.site.register(User, UserAdmin)
