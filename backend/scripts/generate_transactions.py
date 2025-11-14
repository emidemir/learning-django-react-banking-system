import sys
from pathlib import Path
import os
import django

# Setup Django environment
backend_path = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_path)) 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from accounts.models import Account
from transactions.models import Transaction
from decimal import Decimal


def run():

    # === Get main accounts ===
    a10 = Account.objects.get(user__email='u10@g.com')
    a9 = Account.objects.get(user__email='u9@g.com')

    # === Get other single-account users ===
    a3 = Account.objects.get(user__email='u3@g.com')
    a4 = Account.objects.get(user__email='u4@g.com')
    a5 = Account.objects.get(user__email='u5@g.com')
    a6 = Account.objects.get(user__email='u6@g.com')
    a7 = Account.objects.get(user__email='u7@g.com')

    # === Get all accounts of u8 (now 3 accounts) ===
    u8_accounts = list(Account.objects.filter(user__email='u8@g.com'))
    u8_accounts = sorted(u8_accounts, key=lambda acc: acc.account_number)

    a8_main = u8_accounts[0]  # original account
    a8_1 = u8_accounts[1]     # A0008-1
    a8_2 = u8_accounts[2]     # A0008-2


    # ============================
    #      OLD TRANSACTIONS
    # ============================

    transactions = [
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

        # 10 new transactions (original set)
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
            'send_to': a8_main,
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
            'send_from': a8_main,
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
            'send_to': a8_main,
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


    # ============================
    #   NEW TRANSACTIONS FOR u8
    # ============================

    new_u8_transactions = [
        {
            'title': 'Internal Transfer 1',
            'message': 'u8 moves money from debit to credit account',
            'send_from': a8_1,
            'send_to': a8_2,
            'amount': Decimal('200.00'),
        },
        {
            'title': 'Internal Transfer 2',
            'message': 'u8 adjusts money back',
            'send_from': a8_2,
            'send_to': a8_1,
            'amount': Decimal('150.00'),
        },
        {
            'title': 'Consulting Fee',
            'message': 'u6 pays u8 account 1',
            'send_from': a6,
            'send_to': a8_1,
            'amount': Decimal('350.00'),
        },
        {
            'title': 'Gift From Friend',
            'message': 'u5 gives money to u8 account 2',
            'send_from': a5,
            'send_to': a8_2,
            'amount': Decimal('90.00'),
        },
        {
            'title': 'Rent Payment',
            'message': 'u8 pays rent to u4',
            'send_from': a8_1,
            'send_to': a4,
            'amount': Decimal('1200.00'),
        },
        {
            'title': 'Investment Transfer',
            'message': 'u8 invests via account 2',
            'send_from': a8_2,
            'send_to': a7,
            'amount': Decimal('500.00'),
        },
        {
            'title': 'Dinner Reimbursement',
            'message': 'u3 reimburses u8',
            'send_from': a3,
            'send_to': a8_1,
            'amount': Decimal('65.00'),
        },
        {
            'title': 'Shopping Split',
            'message': 'u8 pays u5 back',
            'send_from': a8_2,
            'send_to': a5,
            'amount': Decimal('140.00'),
        },
        {
            'title': 'Freelance Work',
            'message': 'u4 pays u8 for work',
            'send_from': a4,
            'send_to': a8_2,
            'amount': Decimal('800.00'),
        },
        {
            'title': 'Subscription Fee',
            'message': 'u8 pays subscription to u6',
            'send_from': a8_1,
            'send_to': a6,
            'amount': Decimal('30.00'),
        },
    ]

    # Combine them
    transactions.extend(new_u8_transactions)


    # === Create all transactions ===
    for data in transactions:
        Transaction.objects.create(**data)

    print(f"✅ {len(transactions)} transactions created successfully!\n")

    # Display all transactions
    for t in Transaction.objects.all():
        print(f"{t.title} | {t.send_from.user.username} → {t.send_to.user.username} | {t.amount}")


if __name__ == "__main__":
    run()
