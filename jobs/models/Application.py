from django.db import models

from config import settings


class Application(models.Model):
    class Status(models.TextChoices):
        APPLIED     = "applied", "Applied"
        SHORTLISTED = "shortlisted", "Shortlisted"
        REJECTED    = "rejected", "Rejected"
        HIRED       = "hired", "Hired"

    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to="applications/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.APPLIED)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("job", "applicant")
        indexes = [models.Index(fields=["status", "applied_at"])]