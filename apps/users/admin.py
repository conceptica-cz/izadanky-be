from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ("id", "username", "is_staff", "is_active", "is_system", "is_app")
    list_filter = (
        "is_staff",
        "is_system",
        "is_app",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (None, {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_system",
                    "is_app",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_system",
                    "is_app",
                ),
            },
        ),
    )
    search_fields = ("username",)
    ordering = ("username",)
