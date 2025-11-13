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

    # Transactions to create
    transactions = [
        # Original transactions
        {
            'title': 'Payment 1',
            'message': 'Transfer from u10 to u9',
            'send_from': a10,
            'send_to': a9,
            'amount': Decimal('150.75'),
        },
        {
            'title': 'Payment 2',
            'message': 'Refund from u9 to u10',
            'send_from': a9,
            'send_to': a10,
            'amount': Decimal('80.00'),
        },
        {
            'title': 'Payment 3',
            'message': 'Gift from u10 to u9',
            'send_from': a10,
            'send_to': a9,
            'amount': Decimal('250.00'),
        },

        # 10 new transactions (3 related to u10)
        {
            'title': 'Refund A',
            'message': 'Refund from u4 to u10',
            'send_from': a4,
            'send_to': a10,
            'amount': Decimal('120.50'),
        },
        {
            'title': 'Payment B',
            'message': 'Transfer from u10 to u5',
            'send_from': a10,
            'send_to': a5,
            'amount': Decimal('300.00'),
        },
        {
            'title': 'Gift C',
            'message': 'Gift from u7 to u10',
            'send_from': a7,
            'send_to': a10,
            'amount': Decimal('95.25'),
        },

        # Other random transfers
        {
            'title': 'Loan Repayment',
            'message': 'Transfer from u3 to u4',
            'send_from': a3,
            'send_to': a4,
            'amount': Decimal('400.00'),
        },
        {
            'title': 'Investment Payout',
            'message': 'Investment payout from u6 to u8',
            'send_from': a6,
            'send_to': a8,
            'amount': Decimal('600.00'),
        },
        {
            'title': 'Dinner Split',
            'message': 'Dinner payment from u5 to u6',
            'send_from': a5,
            'send_to': a6,
            'amount': Decimal('75.50'),
        },
        {
            'title': 'Loan Transfer',
            'message': 'Loan transfer from u8 to u9',
            'send_from': a8,
            'send_to': a9,
            'amount': Decimal('220.00'),
        },
        {
            'title': 'Salary Payment',
            'message': 'Salary from u4 to u5',
            'send_from': a4,
            'send_to': a5,
            'amount': Decimal('1000.00'),
        },
        {
            'title': 'Bonus',
            'message': 'Bonus from u6 to u7',
            'send_from': a6,
            'send_to': a7,
            'amount': Decimal('500.00'),
        },
        {
            'title': 'Refund X',
            'message': 'Refund from u3 to u8',
            'send_from': a3,
            'send_to': a8,
            'amount': Decimal('60.00'),
        },
        {
            'title': 'Support Transfer',
            'message': 'Support payment from u5 to u3',
            'send_from': a5,
            'send_to': a3,
            'amount': Decimal('180.00'),
        },
    ]

    # Create all transactions
    for data in transactions:
        Transaction.objects.create(**data)

    print("✅ 13 transactions created successfully!\n")

    # Display all transactions
    for t in Transaction.objects.all():
        print(f"{t.send_from.user.username} → {t.send_to.user.username} | {t.amount}")


if __name__ == "__main__":
    run()
