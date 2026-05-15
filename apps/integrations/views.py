from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.customers.models import Customer
from .services import service
@api_view(['GET'])
def health(request): return Response({'aadhaar':'mock-online','pan':'mock-online','ckyc':'mock-online','digilocker':'mock-online'})
@api_view(['POST'])
def ckyc_fetch(request, customer_id):
    c=Customer.objects.get(id=customer_id); return Response(service.ckyc_search(c))
