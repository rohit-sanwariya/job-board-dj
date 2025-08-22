from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from jobs.models import Company
from jobs.serializers.CompanySerializer import CompanySerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

