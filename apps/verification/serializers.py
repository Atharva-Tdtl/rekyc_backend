from rest_framework import serializers
from .models import VerificationCheck
class VerificationCheckSerializer(serializers.ModelSerializer):
    class Meta: model=VerificationCheck; fields='__all__'
