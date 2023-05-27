import pytest

from apps.wallet.exceptions import (InflowTransactionHasANegativeAmount,
                                    InvalidTransactionType,
                                    OutflowTransactionHasAPositiveAmount)
from apps.wallet.validators import (validate_amount_signal_for_type,
                                    validate_flow_type)


def test_signal_amount_validation_for_valid_value() -> None:
    """
    Test valid values of amount depending on transaction type and math signal
    """
    # zeros
    assert validate_amount_signal_for_type(transaction_type='inflow',
                                           transaction_amount=0.00) is None
    assert validate_amount_signal_for_type(transaction_type='outflow',
                                           transaction_amount=0.00) is None
    # positive inflow
    assert validate_amount_signal_for_type(transaction_type='inflow',
                                           transaction_amount=250.00) is None
    # negative outflow
    assert validate_amount_signal_for_type(transaction_type='outflow',
                                           transaction_amount=-550.00) is None


def test_signal_amount_validation_for_invalid_value() -> None:
    """
    Test invalid values of amount depending on transaction type and math signal
    """
    # wrong negative inflow
    with pytest.raises(InflowTransactionHasANegativeAmount):
        assert validate_amount_signal_for_type(transaction_type='inflow',
                                               transaction_amount=-250.00)
    # wrong positive inflow
    with pytest.raises(OutflowTransactionHasAPositiveAmount):
        assert validate_amount_signal_for_type(transaction_type='outflow',
                                               transaction_amount=550.00)


def test_valid_transaction_types() -> None:
    """
    Test valid values for transaction types
    """
    assert validate_flow_type(transaction_type='inflow') is None
    assert validate_flow_type(transaction_type='outflow') is None


def test_invalid_transaction_types() -> None:
    """
    Test invalid values for transaction types
    """
    with pytest.raises(InvalidTransactionType):
        assert validate_flow_type(transaction_type='invalid-type')
    with pytest.raises(InvalidTransactionType):
        assert validate_flow_type(transaction_type='')
