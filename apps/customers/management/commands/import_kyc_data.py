import csv
import os
from django.core.management.base import BaseCommand
from apps.customers.models import Customer
from apps.cases.models import Case
from django.utils.dateparse import parse_date
from django.db import transaction

class Command(BaseCommand):
    help = 'Imports KYC data from the demo dataset CSV'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Path to the CSV file')
        parser.add_argument('--limit', type=int, default=100000, help='Limit number of records')
        parser.add_argument('--clear', action='store_true', help='Clear existing data before import')

    def handle(self, *args, **options):
        path = options['path']
        limit = options['limit']
        clear = options['clear']

        if clear:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Case.objects.all().delete()
            Customer.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Database cleared.'))

        if not path or not os.path.exists(path):
            self.stdout.write(self.style.ERROR(f'File not found at {path}'))
            return

        self.stdout.write(self.style.SUCCESS(f'Starting import from {path}...'))

        with open(path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            
            # We will process in batches of 1000 for safety and speed
            batch_size = 1000
            current_batch = []
            
            for row in reader:
                if count >= limit:
                    break
                
                cust = Customer(
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    mobile=row['mobile'],
                    email=row['email'],
                    dob=parse_date(row['dob']),
                    pan=row['pan_number'],
                    aadhaar_last4=row['aadhaar_masked'][-4:] if row['aadhaar_masked'] else '',
                    customer_type='SALARIED',
                    loan_type=row['loan_type'],
                    status=row['maker_decision'].upper() if row['maker_decision'] else 'DRAFT',
                    risk_category=row['risk_category'].upper() if row['risk_category'] else 'LOW',
                    risk_score=int(row['aml_risk_score']) if row['aml_risk_score'] else 0
                )
                current_batch.append(cust)
                count += 1

                if len(current_batch) >= batch_size:
                    self._save_batch(current_batch)
                    current_batch = []
                    self.stdout.write(f'Imported {count} records...')

            # Save remaining
            if current_batch:
                self._save_batch(current_batch)
                self.stdout.write(f'Imported {count} records...')

            self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} records into MySQL!'))

    def _save_batch(self, batch):
        with transaction.atomic():
            # Use standard save/create for small batches to ensure IDs are generated
            # or use bulk_create and then re-fetch. 
            # For 1000-size batches, bulk_create is fine if we link correctly.
            for cust in batch:
                cust.save()
                Case.objects.create(
                    customer=cust,
                    stage='COMPLETED' if cust.status == 'APPROVED' else 'INTAKE',
                    priority=2 if cust.risk_category == 'HIGH' else 1
                )
