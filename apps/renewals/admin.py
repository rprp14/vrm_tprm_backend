from django.contrib import admin
from .models import Renewal

@admin.register(Renewal)
class RenewalAdmin(admin.ModelAdmin):
    list_display = ('id','status', 'org_id')

    def get_readonly_fields(self, request, obj=None):
        """
        Lock fields once renewal is created
        """
        if obj:
            return [f.name for f in self.model._meta.fields]
        return []

    def has_change_permission(self, request, obj=None):
        """
        Prevent admin from editing renewal after creation
        """
        if obj:
            return False
        return super().has_change_permission(request, obj)
