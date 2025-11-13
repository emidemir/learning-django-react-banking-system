import sys
from pathlib import Path
import os
import django
from decimal import Decimal

# Setup Django environment
backend_path = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_path))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import Account

User = get_user_model()

def run():
    for i in range(3, 9):
        email = f"u{i}@g.com"
        username = f"u{i}"

        user, created = User.objects.get_or_create(
            email=email,
            defaults={'username': username}
        )

        if created:
            user.set_password('1234')
            user.save()
            print(f"✅ Created user {username} with hashed password.")
        else:
            print(f"ℹ️ User {username} already exists.")

        Account.objects.get_or_create(
            user=user,
            defaults={
                'account_number': f"10000{i}",
                'limit': Decimal('1000.00'),
                'balance': Decimal('500.00'),
                'account_type': 'DEBIT',
            }
        )

if __name__ == "__main__":
    run()
