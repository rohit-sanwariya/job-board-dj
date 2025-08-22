from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from jobs.models import Application
from jobs.serializers.ApplicationSerializer import ApplicationSerializer

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

