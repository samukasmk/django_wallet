from apps.wallet.exceptions import InflowTransactionHasANegativeAmount, OutflowTransactionHasAPositiveAmount


def validate_amount_flow_value(transaction_type: str, transaction_amount: float) -> None:
    """ Validate math signal of value for amount field depending on transaction type """
    if transaction_type == 'inflow' and transaction_amount < 0:
        raise InflowTransactionHasANegativeAmount()

    elif transaction_type == 'outflow' and transaction_amount > 0:
        raise OutflowTransactionHasAPositiveAmount()
