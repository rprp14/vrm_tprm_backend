from django.db import models

class Remediation(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("submitted", "Submitted"),
        ("closed", "Closed"),
    ]

    assessment = models.ForeignKey(
        "assessments.Assessment",
        on_delete=models.CASCADE,
        related_name="remediations"
    )

    issue = models.TextField()   # keep this as TEXT
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    org_id = models.IntegerField()
    evidence_uploaded = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Remediation {self.id} - {self.status}"
