from rest_framework import viewsets, decorators, response
from apps.customers.models import Customer
from .models import VerificationCheck
from .serializers import VerificationCheckSerializer
from .services import run_identity, run_address, trigger_field
from apps.audit.services import log_action
class VerificationCheckViewSet(viewsets.ModelViewSet):
    queryset=VerificationCheck.objects.select_related('customer').all().order_by('-created_at'); serializer_class=VerificationCheckSerializer
@decorators.api_view(['POST'])
def run_identity_api(request):
    c=Customer.objects.get(id=request.data.get('customer_id')); chk=run_identity(c); log_action('IDENTITY_VERIFICATION_RUN', chk, request.user, after=VerificationCheckSerializer(chk).data, request=request); return response.Response(VerificationCheckSerializer(chk).data)
@decorators.api_view(['POST'])
def run_address_api(request):
    c=Customer.objects.get(id=request.data.get('customer_id')); chk=run_address(c); log_action('ADDRESS_VERIFICATION_RUN', chk, request.user, after=VerificationCheckSerializer(chk).data, request=request); return response.Response(VerificationCheckSerializer(chk).data)
@decorators.api_view(['POST'])
def trigger_field_api(request):
    c=Customer.objects.get(id=request.data.get('customer_id')); chk=trigger_field(c, request.data.get('reason','Manual trigger')); return response.Response(VerificationCheckSerializer(chk).data)
