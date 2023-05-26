from django.db import models
from apps.wallet.exceptions import (InvalidTransactionType, InflowTransactionHasANegativeAmount,
                                    OutflowTransactionHasAPositiveAmount)


class TransactionType(models.TextChoices):
    INFLOW = 'inflow', 'inflow'
    OUTFLOW = 'outflow', 'outflow'


TRANSACTION_TYPE_CHOICES = [type_code[0] for type_code in TransactionType.choices]


def validate_flow_type(transaction_type: str) -> None:
    if transaction_type not in TRANSACTION_TYPE_CHOICES:
        raise InvalidTransactionType()


def validate_amount_signal_for_type(transaction_type: str, transaction_amount: float) -> None:
    """
    Validate math signal of value for amount field depending on transaction type
    """
    if transaction_type == 'inflow' and transaction_amount < 0:
        raise InflowTransactionHasANegativeAmount()

    elif transaction_type == 'outflow' and transaction_amount > 0:
        raise OutflowTransactionHasAPositiveAmount()
