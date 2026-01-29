from django.contrib import admin
from .models import Remediation

@admin.register(Remediation)
class RemediationAdmin(admin.ModelAdmin):
    list_display = ('id', 'assessment', 'status')

    def get_readonly_fields(self, request, obj=None):
        """
        Admin can NEVER edit remediation fields
        """
        if obj:
            return [f.name for f in self.model._meta.fields]
        return []

    def has_change_permission(self, request, obj=None):
        """
        Completely block admin from saving remediation
        """
        if obj:
            return False
        return super().has_change_permission(request, obj)
