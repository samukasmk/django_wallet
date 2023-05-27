import pytest
from unittest import mock
from rest_framework.exceptions import ValidationError
from apps.wallet.models import FinancialTransaction
from apps.wallet.serializers import FinancialTransactionSerializer
from apps.wallet.tests.conftest import sample_transactions_data, normalize_dict_to_model
from apps.wallet.exceptions import InflowTransactionHasANegativeAmount, OutflowTransactionHasAPositiveAmount
from apps.wallet.serializers import validate_amount_signal_for_type


@pytest.mark.django_db
@pytest.mark.parametrize('transaction_to_create', sample_transactions_data())
def test_serializer_create_single_transactions(transaction_to_create: dict) -> None:
    """
    Test serializer creation with data association for single transactions
    """
    # check first scenery
    assert FinancialTransaction.objects.all().count() == 0

    # check serializer validations without failures
    serializer = FinancialTransactionSerializer(data=transaction_to_create)
    assert serializer.is_valid(raise_exception=True) is True

    # save data on database
    serializer.save()

    # check objects creation on db
    db_transactions = FinancialTransaction.objects.all()
    assert db_transactions.count() == 1

    # check value assignments on objects fields
    created_db_transaction = db_transactions.first()
    assert created_db_transaction is not None

    # compare requests dict with existing model instance
    requested_transaction = normalize_dict_to_model(transaction_to_create)
    for field_name, field_value in requested_transaction.items():
        assert getattr(created_db_transaction, field_name) == field_value


@pytest.mark.django_db
def test_serializer_create_bulk_transactions() -> None:
    """
    Test serializer creation with data association for single transactions
    """
    transactions_to_create = sample_transactions_data()

    # check serializer validations without failures
    serializer = FinancialTransactionSerializer(data=transactions_to_create, many=True)
    assert serializer.is_valid(raise_exception=True) is True

    # save data on database
    serializer.save()

    # check objects creation on db
    db_transactions = FinancialTransaction.objects.all()
    assert db_transactions.count() == len(transactions_to_create)

    # check value assignments on objects fields
    for index_position, created_db_transaction in enumerate(db_transactions):
        # get requested dict
        requested_transaction = transactions_to_create[index_position]

        # compare requests dict with existing model instance
        requested_transaction = normalize_dict_to_model(requested_transaction)

        # check each field of requested dict is equal to model field
        for field_name, field_value in requested_transaction.items():
            assert getattr(created_db_transaction, field_name) == field_value


@pytest.mark.django_db
@mock.patch('apps.wallet.serializers.validate_amount_signal_for_type', side_effect=Exception)
def test_serializer_validation_errors(mock) -> None:
    """
    Test serializer reassignments of ValidationError from validation errors
    """
    # mock validation response with expected exception
    # mocker = mock.patch('apps.wallet.serializers.validate_amount_signal_for_type', 42)

    # get some transaction data to test
    transaction_to_create = sample_transactions_data()[0]

    # check first scenery
    assert FinancialTransaction.objects.all().count() == 0

    # check serializer validations without failures
    serializer = FinancialTransactionSerializer(data=transaction_to_create)

    with pytest.raises(ValidationError):
        assert serializer.is_valid(raise_exception=True)
