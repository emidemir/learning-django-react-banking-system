import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import Account

User = get_user_model()

def run():
    # Create users if they don't exist
    u10, created_10 = User.objects.get_or_create(
        username='u10',
        defaults={'email': 'u10@g.com'}
    )
    if created_10:
        u10.set_password('123123123')
        u10.save()

    u9, created_9 = User.objects.get_or_create(
        username='u9',
        defaults={'email': 'u9@g.com'}
    )
    if created_9:
        u9.set_password('123123123')
        u9.save()

    # Create u8
    u8, created_8 = User.objects.get_or_create(
        username='u8',
        defaults={'email': 'u8@g.com'}
    )
    if created_8:
        u8.set_password('123123123')
        u8.save()

    # Create accounts for u10
    a10, _ = Account.objects.get_or_create(
        user=u10,
        defaults={
            'account_number': 'A0010',
            'limit': 10000,
            'balance': 5000,
            'account_type': Account.AccountType.DEBIT
        }
    )

    # Create accounts for u9
    a9, _ = Account.objects.get_or_create(
        user=u9,
        defaults={
            'account_number': 'A0009',
            'limit': 8000,
            'balance': 4000,
            'account_type': Account.AccountType.DEBIT
        }
    )

    # Create **two accounts for u8**
    a8_1, _ = Account.objects.get_or_create(
        user=u8,
        account_number='A0008-1',
        defaults={
            'limit': 7000,
            'balance': 3500,
            'account_type': Account.AccountType.DEBIT
        }
    )

    a8_2, _ = Account.objects.get_or_create(
        user=u8,
        account_number='A0008-2',
        defaults={
            'limit': 9000,
            'balance': 6000,
            'account_type': Account.AccountType.CREDIT
        }
    )

    print("✅ Accounts created or verified:")
    print(f" - {a10}")
    print(f" - {a9}")
    print(f" - {a8_1}")
    print(f" - {a8_2}")

if __name__ == "__main__":
    run()
