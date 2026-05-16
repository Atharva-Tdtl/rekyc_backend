import os
import django
import random
from faker import Faker
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kyc_platform.settings')
django.setup()

from apps.customers.models import Customer
from apps.cases.models import Case

fake = Faker('en_IN')

def seed_data(total_count=100000, batch_size=5000):
    print(f"Starting seeding of {total_count} records into the live database...")
    
    current_count = 0
    while current_count < total_count:
        customers_to_create = []
        for _ in range(batch_size):
            cust_type = random.choice(['SALARIED', 'SELF_EMPLOYED', 'NRI', 'JOINT'])
            risk_cat = random.choice(['LOW', 'MEDIUM', 'HIGH'])
            status = random.choice(['IN_REVIEW', 'APPROVED', 'REKYC_DUE', 'SUBMITTED'])
            
            customers_to_create.append(Customer(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                mobile=fake.phone_number()[:20],
                email=fake.email(),
                customer_type=cust_type,
                loan_type=random.choice(['Home Loan', 'LAP', 'Top Up']),
                income_monthly=Decimal(random.randint(30000, 500000)),
                status=status,
                risk_category=risk_cat,
                risk_score=random.randint(10, 95)
            ))
        
        # MySQL returns IDs in bulk_create, but we'll use a safer approach for the cases
        Customer.objects.bulk_create(customers_to_create)
        
        # Fetch the last batch of customers to get their IDs
        batch_customers = Customer.objects.all().order_by('-id')[:batch_size]
        
        cases_to_create = []
        for cust in batch_customers:
            stage = random.choice(['INTAKE', 'MAKER_REVIEW', 'CHECKER_REVIEW', 'APPROVED', 'AML_RISK'])
            cases_to_create.append(Case(
                customer_id=cust.id,
                stage=stage,
                priority=random.randint(1, 3)
            ))
        
        Case.objects.bulk_create(cases_to_create)
        
        current_count += batch_size
        print(f"Successfully injected {current_count} / {total_count} records...")

if __name__ == '__main__':
    seed_data()
