from django.db import models

from jobs.models import Job, Skill


class JobSkill(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)

    class Meta:
        unique_together = ("job", "skill")