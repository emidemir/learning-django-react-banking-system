import sys
from pathlib import Path
import os
import django

# Setup Django environment
backend_path = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_path))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import Account
from transactions.models import Transaction

User = get_user_model()

def run():
    confirm = input("⚠️ This will delete ALL Users, Accounts, and Transactions. Type 'YES' to confirm: ")
    if confirm != "YES":
        print("❌ Operation cancelled.")
        return

    print("🧹 Deleting all data...")

    Transaction.objects.all().delete()
    Account.objects.all().delete()
    User.objects.all().delete()

    print("✅ All Users, Accounts, and Transactions have been deleted!")

if __name__ == "__main__":
    run()
