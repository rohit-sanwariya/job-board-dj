from django.urls import path, include
from rest_framework.routers import DefaultRouter
from jobs.views import (
    ApplicationViewSet,
    CompanyViewSet,
    JobSkillViewSet,
    ProfileSkillViewSet,
    SkillViewSet,
    JobViewSet,
)

router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'applications', ApplicationViewSet, basename='application')
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'jobskills', JobSkillViewSet, basename='jobskill')
router.register(r'profileskills', ProfileSkillViewSet, basename='profileskill')
router.register(r'skills', SkillViewSet, basename='skill')

urlpatterns = [
    path('', include(router.urls)),
]
