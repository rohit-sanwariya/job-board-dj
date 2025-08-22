from rest_framework import serializers
from jobs.models.JobSkills import JobSkill

class JobSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSkill
        fields = '__all__'

