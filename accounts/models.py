from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.PositiveIntegerField(unique=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def deposit(self, amt):
        self.balance += amt

    def withdraw(self, amt):
        self.balance -= amt

    def enquiry(self):
        return self.balance

    def __str__(self):
        return str(self.account_number)


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    updated_balance = models.DecimalField(max_digits=12, decimal_places=2)
    deposit = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    withdrawn = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.time.strftime("%Y-%m-%d %H:%M:%S"))
