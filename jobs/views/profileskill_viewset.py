from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from jobs.models import ProfileSkill
from jobs.serializers.ProfileSkillSerializer import ProfileSkillSerializer

class ProfileSkillViewSet(viewsets.ModelViewSet):
    queryset = ProfileSkill.objects.all()
    serializer_class = ProfileSkillSerializer
    permission_classes = [IsAuthenticated]

