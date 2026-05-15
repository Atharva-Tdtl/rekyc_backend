from rest_framework import viewsets, decorators, response
from .models import WorkflowCase, CaseDecision
from .serializers import WorkflowCaseSerializer
from apps.audit.services import log_action
class WorkflowCaseViewSet(viewsets.ModelViewSet):
    queryset=WorkflowCase.objects.select_related('customer').all().order_by('-created_at'); serializer_class=WorkflowCaseSerializer
    @decorators.action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        case=self.get_object(); before={'status':case.status}; case.status='APPROVED'; case.checker=request.user; case.save(); case.customer.status='APPROVED'; case.customer.save(update_fields=['status','updated_at'])
        CaseDecision.objects.create(workflow_case=case,action='APPROVED',remarks=request.data.get('remarks','Approved'),decided_by=request.user)
        log_action('CASE_APPROVED', case, request.user, before=before, after={'status':case.status}, request=request); return response.Response(WorkflowCaseSerializer(case).data)
    @decorators.action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        case=self.get_object(); case.status='REJECTED'; case.checker=request.user; case.save(); case.customer.status='REJECTED'; case.customer.save(update_fields=['status','updated_at'])
        CaseDecision.objects.create(workflow_case=case,action='REJECTED',remarks=request.data.get('remarks','Rejected'),decided_by=request.user)
        return response.Response(WorkflowCaseSerializer(case).data)
    @decorators.action(detail=True, methods=['post'])
    def deficiency(self, request, pk=None):
        case=self.get_object(); case.status='DEFICIENCY'; case.notes=request.data.get('remarks','Document deficiency raised'); case.save()
        CaseDecision.objects.create(workflow_case=case,action='DEFICIENCY',remarks=case.notes,decided_by=request.user)
        return response.Response(WorkflowCaseSerializer(case).data)
