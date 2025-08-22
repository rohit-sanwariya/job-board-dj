# jobs/serializers.py
from rest_framework import serializers

from jobs.models.Job import Job
from jobs.models.Skill import Skill


class JobSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True)

    class Meta:
        model = Job
        fields = [
            "id", "title", "description", "location", "employment_type",
            "salary_min", "salary_max", "company", "skills", "posted_by", "posted_at"
        ]
        read_only_fields = ["posted_by", "posted_at"]
