import pytest
from apps.wallet.validators import validate_amount_flow_value
from apps.wallet.exceptions import InflowTransactionHasANegativeAmount, OutflowTransactionHasAPositiveAmount


def test_valid_zero_inflow_amount() -> None:
    assert validate_amount_flow_value(transaction_type='inflow',
                                      transaction_amount=0.00) is None


def test_valid_zero_outflow_amount() -> None:
    assert validate_amount_flow_value(transaction_type='outflow',
                                      transaction_amount=0.00) is None


def test_valid_positive_inflow_amount() -> None:
    assert validate_amount_flow_value(transaction_type='inflow',
                                      transaction_amount=250.00) is None


def test_valid_negative_outflow_amount() -> None:
    assert validate_amount_flow_value(transaction_type='outflow',
                                      transaction_amount=-550.00) is None


def test_invalid_negative_inflow_amount() -> None:
    with pytest.raises(InflowTransactionHasANegativeAmount):
        assert validate_amount_flow_value(transaction_type='inflow',
                                          transaction_amount=-250.00)


def test_invalid_positive_outflow_amount() -> None:
    with pytest.raises(OutflowTransactionHasAPositiveAmount):
        assert validate_amount_flow_value(transaction_type='outflow',
                                          transaction_amount=550.00)
