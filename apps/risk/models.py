from django.db import models
from apps.customers.models import Customer
class RiskAssessment(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='risk_assessments')
    aml_score=models.IntegerField(default=0); fraud_score=models.IntegerField(default=0); overall_score=models.IntegerField(default=0)
    category=models.CharField(max_length=10, default='LOW'); factors=models.JSONField(default=dict, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
class WatchlistHit(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='watchlist_hits')
    list_type=models.CharField(max_length=50); matched_name=models.CharField(max_length=160); confidence=models.FloatField(default=0); status=models.CharField(max_length=20, default='OPEN')
    created_at=models.DateTimeField(auto_now_add=True)
