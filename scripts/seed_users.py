import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kyc_platform.settings')
django.setup()

from django.contrib.auth.models import User

def create_users():
    users = [
        ('admin', 'admin123', True),
        ('maker_user', 'pass123', False),
        ('checker_user', 'pass123', False),
        ('cxo_user', 'pass123', False),
        ('compliance_user', 'pass123', False),
        ('cust_user', 'pass123', False),
    ]

    for username, password, is_super in users:
        if not User.objects.filter(username=username).exists():
            if is_super:
                User.objects.create_superuser(username=username, password=password, email=f'{username}@example.com')
                print(f'Created Superuser: {username}')
            else:
                User.objects.create_user(username=username, password=password, email=f'{username}@example.com')
                print(f'Created User: {username}')
        else:
            print(f'User {username} already exists')

if __name__ == '__main__':
    create_users()
