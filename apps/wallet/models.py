from django.db import models
from apps.wallet.exceptions import InflowTransactionHasANegativeAmount, OutflowTransactionHasAPositiveAmount

TRANSACTIONS_TYPES = [(1, 'inflow',
                       2, 'outflow')]


class FinancialTransaction(models.Model):
    class TransactionType(models.IntegerChoices):
        inflow = 1
        outflow = 2

    reference = models.CharField(max_length=6, unique=True)
    date = models.DateField()
    amount = models.FloatField()
    type = models.IntegerField(choices=TransactionType.choices)
    category = models.CharField(max_length=250)
    user_email = models.EmailField()

    def validate_amount_flow_value(self):
        if self.type == 1 and self.amount < 0:
            raise InflowTransactionHasANegativeAmount()
        elif self.type == 2 and self.amount > 0:
            raise OutflowTransactionHasAPositiveAmount()

    def save(self, *args, **kwargs):
        self.validate_amount_flow_value()
        return super().save(*args, **kwargs)
