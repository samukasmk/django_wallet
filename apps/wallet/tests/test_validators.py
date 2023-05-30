import pytest
from django.core.exceptions import ValidationError
from apps.wallet.validators import validate_amount_signal_for_type, validate_flow_type, error_messages


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
    with pytest.raises(ValidationError) as exc:
        assert validate_amount_signal_for_type(transaction_type='inflow',
                                               transaction_amount=-250.00)
        assert exc.messages[0] == error_messages['invalid_inflow_amount_value']
    # wrong positive inflow
    with pytest.raises(ValidationError) as exc:
        assert validate_amount_signal_for_type(transaction_type='outflow',
                                               transaction_amount=550.00)
        assert exc.messages[0] == error_messages['invalid_outflow_amount_value']


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
    with pytest.raises(ValidationError) as exc:
        assert validate_flow_type(transaction_type='invalid-type')
        assert exc.messages[0] == error_messages['invalid_transaction_type']
    with pytest.raises(ValidationError):
        assert validate_flow_type(transaction_type='')
        assert exc.messages[0] == error_messages['invalid_transaction_type']
