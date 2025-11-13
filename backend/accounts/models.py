from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    limit = models.DecimalField(max_digits=15, decimal_places=2)
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class AccountType(models.TextChoices):
        DEBIT = 'DEBIT', 'Debit'
        CREDIT = 'CREDIT', 'Credit'
        INVESTMENT = 'INVESTMENT', 'Investment'

    account_type = models.CharField(max_length=10, choices=AccountType.choices, default=AccountType.DEBIT)