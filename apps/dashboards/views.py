from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Avg
from apps.customers.models import Customer
from apps.workflow.models import WorkflowCase
from apps.audit.models import AuditLog
from apps.risk.models import WatchlistHit
from apps.documents.models import KYCDocument
@api_view(['GET'])
def cxo(request):
    total=Customer.objects.count() or 1; approved=Customer.objects.filter(status='APPROVED').count()
    return Response({'total_customers':total,'kyc_completion_rate':round(approved*100/total,2),'compliance_score':98.5,'automation_rate':86.2,'risk_distribution':list(Customer.objects.values('risk_category').annotate(count=Count('id'))),'fraud_watchlist_hits':WatchlistHit.objects.count()})
@api_view(['GET'])
def operations(request):
    return Response({'pending_cases':WorkflowCase.objects.exclude(status__in=['APPROVED','REJECTED']).count(),'rekyc_alerts':Customer.objects.filter(status='REKYC_DUE').count(),'document_deficiencies':KYCDocument.objects.filter(status='DEFICIENT').count(),'avg_risk_score':Customer.objects.aggregate(v=Avg('risk_score'))['v'] or 0})
@api_view(['GET'])
def compliance(request):
    return Response({'audit_events':AuditLog.objects.count(),'regulatory_reports':[{'name':'RBI KYC Master Direction','status':'Ready'},{'name':'PMLA AML Monitoring','status':'Ready'},{'name':'DPDP Consent Traceability','status':'Ready'}],'high_risk_customers':Customer.objects.filter(risk_category='HIGH').count(),'open_watchlist_hits':WatchlistHit.objects.filter(status='OPEN').count()})
