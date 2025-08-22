from rest_framework import serializers
from jobs.models.Company import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

