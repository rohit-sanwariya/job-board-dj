from django.db import models
from django.conf import settings

class Company(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="companies")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

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

class Application(models.Model):
    class Status(models.TextChoices):
        APPLIED     = "applied", "Applied"
        SHORTLISTED = "shortlisted", "Shortlisted"
        REJECTED    = "rejected", "Rejected"
        HIRED       = "hired", "Hired"

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to="applications/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.APPLIED)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("job", "applicant")
        indexes = [models.Index(fields=["status", "applied_at"])]

class JobSkill(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("job", "skill")

# Link Profile <-> Skill via a through table, from accounts.Profile to avoid circular import:
from accounts.models import Profile  # noqa: E402

class ProfileSkill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("profile", "skill")
