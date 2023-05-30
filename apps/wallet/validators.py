from django.db import models
from django.core.exceptions import ValidationError


# Transaction type codes
class TransactionType(models.TextChoices):
    INFLOW = 'inflow', 'inflow'
    OUTFLOW = 'outflow', 'outflow'


TRANSACTION_TYPE_CHOICES = [type_code[0] for type_code in TransactionType.choices]

# known validation errors
error_messages = {
    'invalid_transaction_type': ('Invalid transaction type, please provide '
                                 'a valid value like "inflow" or "outflow"'),
    'invalid_inflow_amount_value': ('Inflow transactions can not have negative values '
                                    'in the "amount" field, please provide a positive value.'),
    'invalid_outflow_amount_value': ('Outflow transactions can not have positive values '
                                     'in the "amount" field, please provide a negative value.')
}


def validate_flow_type(transaction_type: str) -> None:
    if transaction_type not in TRANSACTION_TYPE_CHOICES:
        raise ValidationError(error_messages['invalid_transaction_type'])


def validate_amount_signal_for_type(transaction_type: str, transaction_amount: float) -> None:
    """
    Validate math signal of value for amount field depending on transaction type
    """
    if transaction_type == 'inflow' and transaction_amount < 0:
        raise ValidationError({'amount': error_messages['invalid_inflow_amount_value']})

    elif transaction_type == 'outflow' and transaction_amount > 0:
        raise ValidationError({'amount': error_messages['invalid_outflow_amount_value']})
