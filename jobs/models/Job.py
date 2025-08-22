from django.db import  models

from config import settings
from jobs.models.Company import Company


class Job(models.Model):
    class EmploymentType(models.TextChoices):
        FULL_TIME = "full_time", "Full-time"
        PART_TIME = "part_time", "Part-time"
        CONTRACT   = "contract", "Contract"
        INTERN     = "intern", "Intern"
        TEMP       = "temp", "Temporary"

    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    location = models.CharField(max_length=255, db_index=True)
    employment_type = models.CharField(max_length=20, choices=EmploymentType.choices)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posted_jobs")

    skills = models.ManyToManyField("Skill", through="JobSkill", related_name="jobs")

    class Meta:
        indexes = [
            models.Index(fields=["location", "employment_type"]),
            models.Index(fields=["-posted_at"]),
        ]

    def __str__(self):
        return self.title