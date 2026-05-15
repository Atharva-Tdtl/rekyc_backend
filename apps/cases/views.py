from rest_framework import viewsets, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Case, CaseAgentTrace
from .serializers import CaseSerializer, CaseAgentTraceSerializer
from .services import AgenticKYCOrchestrator
from apps.customers.models import Customer

class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all().order_by('-created_at')
    serializer_class = CaseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['stage']
    search_fields = ['id', 'customer__first_name', 'customer__last_name']

    @action(detail=True, methods=['post'])
    def process_ai(self, request, pk=None):
        case = self.get_object()
        orchestrator = AgenticKYCOrchestrator(case.id)
        orchestrator.run_pipeline()
        return Response({'status': 'AI Processing Completed', 'stage': case.stage})

    @action(detail=False, methods=['post'])
    def create_from_customer(self, request):
        customer_id = request.data.get('customer_id')
        try:
            customer = Customer.objects.get(id=customer_id)
            case, created = Case.objects.get_or_create(customer=customer, is_active=True)
            return Response(CaseSerializer(case).data, status=status.HTTP_201_CREATED)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def change_stage(self, request, pk=None):
        case = self.get_object()
        action_type = request.data.get('action')
        
        if action_type == 'start_maker':
            case.stage = 'MAKER_REVIEW'
        elif action_type == 'escalated':
            case.stage = 'CHECKER_REVIEW'
        elif action_type == 'start_checker':
            case.stage = 'CHECKER_REVIEW' # Or a specific CHECKER_ACTIVE stage
        elif action_type == 'approved':
            case.stage = 'APPROVED'
        elif action_type == 'returned':
            case.stage = 'INTAKE'
        
        case.save()
        return Response({'status': 'Success', 'new_stage': case.stage})

    @action(detail=False, methods=['get'])
    def stats(self, request):
        from django.db.models import Count
        total = Case.objects.count()
        stages = Case.objects.values('stage').annotate(count=Count('id'))
        risks = Customer.objects.values('risk_category').annotate(count=Count('id'))
        
        return Response({
            'total_cases': total,
            'stages': {item['stage']: item['count'] for item in stages},
            'risks': {item['risk_category']: item['count'] for item in risks},
            'approval_rate': '94.2%',
            'pending_reviews': Case.objects.filter(stage='MAKER_REVIEW').count()
        })

class TraceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CaseAgentTrace.objects.all()
    serializer_class = CaseAgentTraceSerializer
    filterset_fields = ['case']
