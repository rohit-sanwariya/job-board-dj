from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from jobs.models import JobSkill
from jobs.serializers.JobSkillSerializer import JobSkillSerializer

class JobSkillViewSet(viewsets.ModelViewSet):
    queryset = JobSkill.objects.all()
    serializer_class = JobSkillSerializer
    permission_classes = [IsAuthenticated]

