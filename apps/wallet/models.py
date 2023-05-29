from django.db import models

from apps.wallet.validators import (TransactionType,
                                    validate_amount_signal_for_type,
                                    validate_flow_type)


class FinancialTransaction(models.Model):
    reference = models.CharField(max_length=6, unique=True)
    date = models.DateField()
    amount = models.DecimalField(max_digits=33, decimal_places=2)
    type = models.CharField(max_length=7, choices=TransactionType.choices)
    category = models.CharField(max_length=250)
    user_email = models.EmailField()

    def save(self, *args, **kwargs) -> None:
        """
        Data validation before to saving on db
        """
        validate_flow_type(transaction_type=self.type)
        validate_amount_signal_for_type(transaction_type=self.type, transaction_amount=self.amount)
        return super().save(*args, **kwargs)

    def to_dict(self) -> dict:
        """
        Create new dict object from this model instance just represent it for manual querying
        """
        return {'reference': self.reference,
                'date': str(self.date),
                'amount': self.amount,
                'type': self.get_type_display().lower(),
                'category': self.category,
                'user_email': self.user_email}

    def __str__(self) -> str:
        return str(self.to_dict())
