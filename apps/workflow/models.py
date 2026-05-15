from django.db import models
from django.conf import settings
from apps.customers.models import Customer
class WorkflowCase(models.Model):
    STATUS=[('OPEN','Open'),('IN_REVIEW','In Review'),('APPROVED','Approved'),('REJECTED','Rejected'),('DEFICIENCY','Deficiency'),('EDD','Enhanced Due Diligence')]
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='workflow_cases')
    title=models.CharField(max_length=200); status=models.CharField(max_length=20,choices=STATUS,default='OPEN')
    priority=models.CharField(max_length=20, default='MEDIUM')
    maker=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL, related_name='maker_cases')
    checker=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL, related_name='checker_cases')
    notes=models.TextField(blank=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
class CaseDecision(models.Model):
    workflow_case=models.ForeignKey(WorkflowCase,on_delete=models.CASCADE,related_name='decisions')
    action=models.CharField(max_length=40); remarks=models.TextField(blank=True)
    decided_by=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.SET_NULL)
    created_at=models.DateTimeField(auto_now_add=True)
