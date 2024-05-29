from rest_framework import serializers
from .models import Company
"""creating serializer to validate the data"""
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
