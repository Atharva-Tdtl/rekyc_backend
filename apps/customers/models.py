from django.db import models
from django.conf import settings

class Customer(models.Model):
    CUSTOMER_TYPES=[('SALARIED','Salaried'),('SELF_EMPLOYED','Self Employed'),('NRI','NRI'),('JOINT','Joint Applicant')]
    STATUS=[('DRAFT','Draft'),('SUBMITTED','Submitted'),('IN_REVIEW','In Review'),('APPROVED','Approved'),('REJECTED','Rejected'),('REKYC_DUE','Re-KYC Due')]
    RISK=[('LOW','Low'),('MEDIUM','Medium'),('HIGH','High')]
    first_name=models.CharField(max_length=80); last_name=models.CharField(max_length=80, blank=True)
    mobile=models.CharField(max_length=20); email=models.EmailField(blank=True)
    dob=models.DateField(null=True, blank=True); pan=models.CharField(max_length=12, blank=True); aadhaar_last4=models.CharField(max_length=4, blank=True)
    customer_type=models.CharField(max_length=20, choices=CUSTOMER_TYPES, default='SALARIED')
    loan_type=models.CharField(max_length=50, default='Home Loan')
    current_address=models.TextField(blank=True); permanent_address=models.TextField(blank=True)
    property_address=models.TextField(blank=True); builder_name=models.CharField(max_length=120, blank=True)
    income_monthly=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status=models.CharField(max_length=20, choices=STATUS, default='DRAFT')
    risk_category=models.CharField(max_length=10, choices=RISK, default='LOW')
    risk_score=models.IntegerField(default=0)
    assigned_to=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL, related_name='assigned_customers')
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL, related_name='created_customers')
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    def __str__(self): return f'{self.first_name} {self.last_name}'

class CoApplicant(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='co_applicants')
    name=models.CharField(max_length=160); relation=models.CharField(max_length=60); pan=models.CharField(max_length=12, blank=True); mobile=models.CharField(max_length=20, blank=True)
