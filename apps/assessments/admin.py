from django.contrib import admin
from .models import Assessment

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'org_id')

    def get_readonly_fields(self, request, obj=None):
        """
        Lock ALL fields once assessment is submitted or beyond
        """
        if obj and obj.status != 'draft':
            return [f.name for f in self.model._meta.fields]
        return []

    def has_change_permission(self, request, obj=None):
        """
        Completely block saving changes after submission
        """
        if obj and obj.status != 'draft':
            return False
        return super().has_change_permission(request, obj)
