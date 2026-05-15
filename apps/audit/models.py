from django.conf import settings
from django.db import models

class AuditLog(models.Model):
    action=models.CharField(max_length=120)
    entity_type=models.CharField(max_length=80)
    entity_id=models.CharField(max_length=80, blank=True)
    actor=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL)
    before=models.JSONField(default=dict, blank=True)
    after=models.JSONField(default=dict, blank=True)
    ip_address=models.GenericIPAddressField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
