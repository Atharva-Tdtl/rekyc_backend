from rest_framework import viewsets, decorators, response
from .models import Customer
from .serializers import CustomerSerializer
from apps.audit.services import log_action
from apps.workflow.services import create_case_for_customer
class CustomerViewSet(viewsets.ModelViewSet):
    queryset=Customer.objects.all().order_by('-created_at'); serializer_class=CustomerSerializer
    def perform_create(self, serializer):
        obj=serializer.save(); log_action('CUSTOMER_CREATED', obj, self.request.user, after=CustomerSerializer(obj).data, request=self.request)
    @decorators.action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        c=self.get_object(); before={'status':c.status}; c.status='SUBMITTED'; c.save(update_fields=['status','updated_at'])
        case=create_case_for_customer(c, request.user)
        log_action('CUSTOMER_SUBMITTED', c, request.user, before=before, after={'status':c.status,'case_id':case.id}, request=request)
        return response.Response({'status':c.status,'case_id':case.id})
