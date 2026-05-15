from django.db import models
from apps.customers.models import Customer
class Notification(models.Model):
    CHANNELS=[('SMS','SMS'),('EMAIL','Email'),('WHATSAPP','WhatsApp')]
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='notifications')
    channel=models.CharField(max_length=20,choices=CHANNELS); template=models.CharField(max_length=100); message=models.TextField(); status=models.CharField(max_length=20,default='QUEUED')
    created_at=models.DateTimeField(auto_now_add=True); sent_at=models.DateTimeField(null=True,blank=True)
