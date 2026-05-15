import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kyc_platform.settings')
django.setup()

from django.core.mail import send_mail

try:
    print("Attempting to send test email...")
    send_mail(
        'Test SMTP Connection',
        'If you see this, your SMTP settings are correct!',
        None,
        ['appsupport@tdtl.world'],
        fail_silently=False,
    )
    print("SUCCESS: Email sent successfully!")
except Exception as e:
    print(f"FAILED: {str(e)}")
