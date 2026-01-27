from django.db import models
from apps.assessments.models import Assessment

class Renewal(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("triggered", "Triggered"),
        ("completed", "Completed"),
    ]

    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="renewals"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    org_id = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Renewal {self.id} - {self.status}"
