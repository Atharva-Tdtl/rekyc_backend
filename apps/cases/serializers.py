from rest_framework import serializers
from .models import Case, CaseAgentTrace
from apps.customers.models import Customer

class CaseAgentTraceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseAgentTrace
        fields = '__all__'

class CaseSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.__str__', read_only=True)
    loan_type = serializers.CharField(source='customer.loan_type', read_only=True)
    customer_type = serializers.CharField(source='customer.customer_type', read_only=True)
    risk_category = serializers.CharField(source='customer.risk_category', read_only=True)
    pan = serializers.CharField(source='customer.pan', read_only=True)
    aadhaar_last4 = serializers.CharField(source='customer.aadhaar_last4', read_only=True)
    mobile = serializers.CharField(source='customer.mobile', read_only=True)
    email = serializers.CharField(source='customer.email', read_only=True)
    traces = CaseAgentTraceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Case
        fields = ['id', 'customer', 'customer_name', 'loan_type', 'customer_type', 'risk_category', 'pan', 'aadhaar_last4', 'mobile', 'email', 'stage', 'is_active', 'priority', 'assigned_to', 'created_at', 'updated_at', 'traces']
