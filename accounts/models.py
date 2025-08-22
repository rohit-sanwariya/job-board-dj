from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    class Role(models.TextChoices):
        EMPLOYER = "employer", "Employer"
        JOBSEEKER = "jobseeker", "Job Seeker"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.JOBSEEKER)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)
    education = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    # skills m2m is defined from jobs.ProfileSkill to avoid circular imports

    def __str__(self):
        return f"{self.user.username} Profile"
