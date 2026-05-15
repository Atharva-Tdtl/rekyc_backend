from django.db import models
from apps.customers.models import Customer
class VerificationCheck(models.Model):
    CHECK_TYPES=[('IDENTITY','Identity'),('ADDRESS','Address'),('FACE_MATCH','Face Match'),('LIVENESS','Liveness'),('FIELD','Field'),('VIDEO_KYC','Video KYC')]
    STATUS=[('PENDING','Pending'),('PASSED','Passed'),('FAILED','Failed'),('REVIEW','Review Required')]
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='verification_checks')
    check_type=models.CharField(max_length=30, choices=CHECK_TYPES); status=models.CharField(max_length=20, choices=STATUS, default='PENDING')
    score=models.FloatField(default=0); remarks=models.TextField(blank=True); evidence=models.JSONField(default=dict, blank=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
