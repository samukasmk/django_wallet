from django.db import models
from apps.wallet.validators import validate_amount_flow_value


class TransactionType(models.TextChoices):
    INFLOW = 'inflow', 'inflow'
    OUTFLOW = 'outflow', 'outflow'


class FinancialTransaction(models.Model):
    reference = models.CharField(max_length=6, unique=True)
    date = models.DateField()
    amount = models.FloatField()
    type = models.CharField(max_length=7, choices=TransactionType.choices)
    category = models.CharField(max_length=250)
    user_email = models.EmailField()

    def save(self, *args, **kwargs) -> None:
        validate_amount_flow_value(transaction_type=self.type,
                                   transaction_amount=self.amount)
        return super().save(*args, **kwargs)

    def to_dict(self) -> dict:
        """ Format to dict normalizing fields response as str """
        return {'reference': self.reference,
                'date': self.date.strftime('%Y-%m-%d'),
                'amount': '{:.2f}'.format(self.amount),
                'type': self.get_type_display().lower(),
                'category': self.category,
                'user_email': self.user_email}

    def __str__(self) -> str:
        return str(self.to_dict())
