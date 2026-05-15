from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.mail import send_mail
from .serializers import UserSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        # Map groups or custom fields to roles
        if user.is_superuser: token['role'] = 'Operations Manager'
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {'username': self.user.username, 'email': self.user.email}
        # Simplified role logic for demo
        username = self.user.username
        if username == 'admin' or username == 'ops_user': data['role'] = 'Operations Manager'
        elif username == 'cxo_user': data['role'] = 'CXO'
        elif username == 'compliance_user': data['role'] = 'Compliance Officer'
        elif username == 'maker_user': data['role'] = 'Maker'
        elif username == 'checker_user': data['role'] = 'Checker'
        else: data['role'] = 'Customer'
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
# ... (rest of the file)
@permission_classes([AllowAny])
def send_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    
    if not email or not otp:
        return Response({"error": "Email and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    subject = "Your KYC Verification Code"
    message = f"Hello,\n\nYour 6-digit verification code for KYC Shield is: {otp}\n\nPlease enter this code in the portal to continue your registration.\n\nThank you,\nKYC Shield Team"
    
    try:
        send_mail(subject, message, None, [email])
        return Response({"message": "Email sent successfully"})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
