from rest_framework import serializers
from .models import WorkflowCase, CaseDecision
class CaseDecisionSerializer(serializers.ModelSerializer):
    decided_by_name=serializers.CharField(source='decided_by.username', read_only=True)
    class Meta: model=CaseDecision; fields='__all__'
class WorkflowCaseSerializer(serializers.ModelSerializer):
    customer_name=serializers.CharField(source='customer.__str__', read_only=True)
    decisions=CaseDecisionSerializer(many=True, read_only=True)
    class Meta: model=WorkflowCase; fields='__all__'
