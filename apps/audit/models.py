from django.db import models

class AuditLog(models.Model):
    actor = models.CharField(max_length=100)
    action = models.CharField(max_length=50)
    entity = models.CharField(max_length=50)
    entity_id = models.IntegerField(null=True)
    org_id = models.IntegerField()
    success = models.BooleanField(default=True)
    message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
