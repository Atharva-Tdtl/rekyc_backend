from django.db import models
from apps.customers.models import Customer
class KYCDocument(models.Model):
    TYPES=[('AADHAAR','Aadhaar'),('PAN','PAN'),('PASSPORT','Passport'),('DRIVING_LICENSE','Driving License'),('VOTER_ID','Voter ID'),('UTILITY_BILL','Utility Bill'),('BANK_STATEMENT','Bank Statement'),('SALARY_SLIP','Salary Slip'),('PROPERTY_DOC','Property Document'),('SELFIE','Selfie')]
    STATUS=[('UPLOADED','Uploaded'),('PROCESSED','Processed'),('FAILED','Failed'),('DEFICIENT','Deficient')]
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='documents')
    doc_type=models.CharField(max_length=40,choices=TYPES); file=models.FileField(upload_to='kyc_docs/', blank=True, null=True)
    file_name=models.CharField(max_length=255, blank=True); status=models.CharField(max_length=20, choices=STATUS, default='UPLOADED')
    extracted_data=models.JSONField(default=dict, blank=True); confidence=models.FloatField(default=0)
    deficiency_reason=models.TextField(blank=True); uploaded_at=models.DateTimeField(auto_now_add=True); processed_at=models.DateTimeField(null=True,blank=True)
