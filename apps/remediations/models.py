from django.db import models

class Remediation(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("closed", "Closed"),
    ]

    assessment = models.ForeignKey(
        "assessments.Assessment",
        on_delete=models.CASCADE,
        related_name="remediations"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    org_id = models.IntegerField()
    evidence_uploaded = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
