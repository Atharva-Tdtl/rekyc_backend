from django.utils import timezone
from rest_framework import viewsets, decorators, response
from .models import Notification
from .serializers import NotificationSerializer
class NotificationViewSet(viewsets.ModelViewSet):
    queryset=Notification.objects.all().order_by('-created_at'); serializer_class=NotificationSerializer
    @decorators.action(detail=True, methods=['post'])
    def send_mock(self, request, pk=None):
        n=self.get_object(); n.status='SENT'; n.sent_at=timezone.now(); n.save(); return response.Response(NotificationSerializer(n).data)
