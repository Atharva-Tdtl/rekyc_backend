from rest_framework import serializers
from .models import Customer, CoApplicant
class CoApplicantSerializer(serializers.ModelSerializer):
    class Meta: model=CoApplicant; fields='__all__'; read_only_fields=['customer']
class CustomerSerializer(serializers.ModelSerializer):
    co_applicants=CoApplicantSerializer(many=True, required=False)
    assigned_to_name=serializers.CharField(source='assigned_to.username', read_only=True)
    class Meta: model=Customer; fields='__all__'; read_only_fields=['created_by','risk_score','risk_category']
    def create(self, validated_data):
        cos=validated_data.pop('co_applicants', [])
        request=self.context.get('request')
        c=Customer.objects.create(created_by=getattr(request,'user',None), **validated_data)
        for co in cos: CoApplicant.objects.create(customer=c, **co)
        return c
