from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "role", "org_id", "is_staff")
    list_filter = ("role", "org_id")
class CustomUserAdmin(UserAdmin):

    def has_module_permission(self, request):
        if request.user.role == 'Vendor':
            return False
        return super().has_module_permission(request)