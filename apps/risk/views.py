from rest_framework import viewsets, decorators, response
from apps.customers.models import Customer
from .models import RiskAssessment, WatchlistHit
from .serializers import RiskAssessmentSerializer, WatchlistHitSerializer
from .services import calculate_risk, fraud_detection
from apps.audit.services import log_action
class RiskAssessmentViewSet(viewsets.ReadOnlyModelViewSet): queryset=RiskAssessment.objects.all().order_by('-created_at'); serializer_class=RiskAssessmentSerializer
class WatchlistHitViewSet(viewsets.ModelViewSet): queryset=WatchlistHit.objects.all().order_by('-created_at'); serializer_class=WatchlistHitSerializer
@decorators.api_view(['POST'])
def score_customer(request, customer_id):
    c=Customer.objects.get(id=customer_id); r=calculate_risk(c); log_action('RISK_SCORE_GENERATED', r, request.user, after=RiskAssessmentSerializer(r).data, request=request); return response.Response(RiskAssessmentSerializer(r).data)
@decorators.api_view(['POST'])
def fraud_customer(request, customer_id):
    c=Customer.objects.get(id=customer_id); return response.Response(fraud_detection(c))
