from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from jobs.models import Skill
from jobs.serializers.SkillSerializer import SkillSerializer

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]

