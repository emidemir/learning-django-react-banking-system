from django.db import models

# Create your models here.
class Transaction(models.Model):
    title = models.CharField(max_length=50)
    message = models.TextField(max_length=300)
    
    send_from = models.OneToOneField("accounts.Account", related_name="account_from", null=True, on_delete=models.SET_NULL)
    send_to = models.OneToOneField("accounts.Account", related_name="account_to", null=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date_time = models.DateTimeField(auto_now_add=True)