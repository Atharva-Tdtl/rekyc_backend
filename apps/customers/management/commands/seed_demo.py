from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from faker import Faker
from apps.customers.models import Customer
from apps.documents.models import KYCDocument
from apps.documents.services import mock_ocr_extract
from apps.verification.services import run_identity, run_address
from apps.risk.services import calculate_risk
from apps.workflow.services import create_case_for_customer
import random

class Command(BaseCommand):
    help='Seed demo data for KYC/Re-KYC PoC'
    def handle(self,*args,**kwargs):
        roles=['Admin','Operations','Compliance','CXO','Field Agent','Branch User']
        for r in roles: Group.objects.get_or_create(name=r)
        users=[('admin','Admin@123','Admin'),('ops_user','Ops@123','Operations'),('compliance_user','Compliance@123','Compliance'),('cxo_user','Cxo@123','CXO'),('field_agent','Field@123','Field Agent')]
        for u,p,g in users:
            user,_=User.objects.get_or_create(username=u, defaults={'email':f'{u}@demo.local','is_staff':u=='admin','is_superuser':u=='admin'})
            user.set_password(p); user.save(); user.groups.add(Group.objects.get(name=g))
        fake=Faker('en_IN')
        if Customer.objects.count()<50:
            for i in range(50):
                c=Customer.objects.create(first_name=fake.first_name(),last_name=fake.last_name(),mobile=fake.msisdn()[:10],email=fake.email(),dob=fake.date_of_birth(minimum_age=22,maximum_age=70),pan=f'ABCDE{1000+i}F',aadhaar_last4=str(1000+i)[-4:],customer_type=random.choice(['SALARIED','SELF_EMPLOYED','NRI']),loan_type=random.choice(['Home Loan','LAP','Construction Loan']),current_address=fake.address(),permanent_address=fake.address(),property_address=fake.address(),builder_name=random.choice(['ABC Builders','Urban Homes','']),income_monthly=random.randint(35000,800000),status=random.choice(['SUBMITTED','IN_REVIEW','APPROVED','REKYC_DUE']))
                for dt in ['PAN','AADHAAR','BANK_STATEMENT']:
                    d=KYCDocument.objects.create(customer=c,doc_type=dt,file_name=f'{dt.lower()}_{c.id}.pdf'); mock_ocr_extract(d)
                run_identity(c); run_address(c); calculate_risk(c); create_case_for_customer(c)
        self.stdout.write(self.style.SUCCESS('Demo users and KYC records created.'))
