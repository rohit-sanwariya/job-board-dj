from rest_framework import serializers
from jobs.models.ProfileSkill import ProfileSkill

class ProfileSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileSkill
        fields = '__all__'

