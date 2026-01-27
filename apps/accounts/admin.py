from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "role", "org_id", "is_staff")
    list_filter = ("role", "org_id")
