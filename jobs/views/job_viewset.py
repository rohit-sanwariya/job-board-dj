from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from jobs.models import Job
from jobs.search import search_jobs
from jobs.serializers.JobSerializer import JobSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # automatically set posted_by to the logged-in user
        serializer.save(posted_by=self.request.user)

    @action(detail=False, methods=["get"])
    def search(self, request):
        query = request.GET.get("q", "")
        results = search_jobs(query)
        return Response(results)