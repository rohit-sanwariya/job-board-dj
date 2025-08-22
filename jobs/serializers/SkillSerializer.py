from rest_framework import serializers
from jobs.models.Skill import Skill

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

