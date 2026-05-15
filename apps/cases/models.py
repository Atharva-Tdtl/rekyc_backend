from django.db import models
from django.conf import settings
from apps.customers.models import Customer

class Case(models.Model):
    STAGES = [
        ('INTAKE', 'Intake'),
        ('MAKER_REVIEW', 'Maker Review'),
        ('CHECKER_REVIEW', 'Checker Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('OCR_EXTRACTION', 'OCR & Extraction'),
        ('IDENTITY_VERIF', 'Identity Verification'),
        ('ADDRESS_VERIF', 'Address Verification'),
        ('AML_RISK', 'AML Risk Scoring'),
        ('COMPLIANCE_REVIEW', 'Compliance Review'),
        ('CKYC_UPLOAD', 'CKYC Upload'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cases')
    stage = models.CharField(max_length=30, choices=STAGES, default='INTAKE')
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=1) # 1: Normal, 2: High, 3: Critical
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Case {self.id} - {self.customer.first_name} ({self.stage})"

class CaseAgentTrace(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='traces')
    agent_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    log = models.TextField()
    thought = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
