from rest_framework import serializers
from .models import KYCDocument
class KYCDocumentSerializer(serializers.ModelSerializer):
    customer_name=serializers.CharField(source='customer.__str__', read_only=True)
    class Meta: model=KYCDocument; fields='__all__'
