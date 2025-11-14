import sys
from pathlib import Path
import os
import django

# Setup Django environment
backend_path = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_path)) # Python will look at this folder first when looking for config.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # Replace 'config' with your project folder
django.setup()
from accounts.models import Account
from transactions.models import Transaction
from decimal import Decimal

def run():

    # Get main accounts
    a10 = Account.objects.get(user__email='u10@g.com')
    a9 = Account.objects.get(user__email='u9@g.com')

    # Get other accounts
    a3 = Account.objects.get(user__email='u3@g.com')
    a4 = Account.objects.get(user__email='u4@g.com')
    a5 = Account.objects.get(user__email='u5@g.com')
    a6 = Account.objects.get(user__email='u6@g.com')
    a7 = Account.objects.get(user__email='u7@g.com')
    a8 = Account.objects.get(user__email='u8@g.com')

    transactions_u8 = [
    # Outgoing from u8
    {"title": "Groceries", "message": "Payment to u7", "send_from": a8, "send_to": a7, "amount": Decimal("45.20")},
    {"title": "Loan Repayment", "message": "Sent to u6", "send_from": a8, "send_to": a6, "amount": Decimal("120.00")},
    {"title": "Dinner", "message": "Paid to u5", "send_from": a8, "send_to": a5, "amount": Decimal("32.50")},
    {"title": "Gift", "message": "Birthday gift to u3", "send_from": a8, "send_to": a3, "amount": Decimal("75.00")},
    {"title": "Phone Bill Split", "message": "Sent to u4", "send_from": a8, "send_to": a4, "amount": Decimal("18.99")},
    {"title": "Online Purchase", "message": "Sent to u9", "send_from": a8, "send_to": a9, "amount": Decimal("210.00")},
    {"title": "Transport Fee", "message": "Sent to u10", "send_from": a8, "send_to": a10, "amount": Decimal("14.75")},
    {"title": "Rent Share", "message": "Sent to u7", "send_from": a8, "send_to": a7, "amount": Decimal("650.00")},
    {"title": "Utility Bill", "message": "Paid to u6", "send_from": a8, "send_to": a6, "amount": Decimal("54.40")},
    {"title": "Gym Split", "message": "Sent to u5", "send_from": a8, "send_to": a5, "amount": Decimal("29.99")},

    # Incoming to u8
    {"title": "Refund", "message": "Refund from u7", "send_from": a7, "send_to": a8, "amount": Decimal("45.20")},
    {"title": "Loan Return", "message": "u6 paid back", "send_from": a6, "send_to": a8, "amount": Decimal("50.00")},
    {"title": "Gift", "message": "Gift from u5", "send_from": a5, "send_to": a8, "amount": Decimal("120.00")},
    {"title": "Payment Split", "message": "u3 shared cost", "send_from": a3, "send_to": a8, "amount": Decimal("30.00")},
    {"title": "Cashback", "message": "Received from u4", "send_from": a4, "send_to": a8, "amount": Decimal("12.00")},
    {"title": "Side Job", "message": "Paid by u9", "send_from": a9, "send_to": a8, "amount": Decimal("200.00")},
    {"title": "Transport Refund", "message": "Received from u10", "send_from": a10, "send_to": a8, "amount": Decimal("14.75")},
    {"title": "Meal Refund", "message": "u7 paid back", "send_from": a7, "send_to": a8, "amount": Decimal("32.50")},
    {"title": "Deposit", "message": "Received from u6", "send_from": a6, "send_to": a8, "amount": Decimal("75.00")},
    {"title": "Share Split", "message": "u5 paid extra share", "send_from": a5, "send_to": a8, "amount": Decimal("21.80")},
]
    
    # Create all transactions
    for data in transactions_u8:
        Transaction.objects.create(**data)

    print("✅ 13 transactions created successfully!\n")

    # Display all transactions
    for t in Transaction.objects.all():
        print(f"{t.send_from.user.username} → {t.send_to.user.username} | {t.amount}")


if __name__ == "__main__":
    run()
