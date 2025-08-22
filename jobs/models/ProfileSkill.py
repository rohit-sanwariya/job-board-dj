from django.db import models

from jobs.models import Skill
from users.models import Profile


class ProfileSkill(models.Model):
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)

    class Meta:
        unique_together = ("profile", "skill")