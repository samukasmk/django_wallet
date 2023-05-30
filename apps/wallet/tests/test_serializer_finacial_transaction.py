from typing import Sequence
from unittest import mock

import pytest
from rest_framework.exceptions import ValidationError

from apps.wallet.models import FinancialTransaction
from apps.wallet.serializers import FinancialTransactionSerializer
from apps.wallet.validators import error_messages
from apps.wallet.tests.conftest import sample_transactions_data


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
    for json_field_name, json_field_value in transaction_to_create.items():
        db_field = getattr(created_db_transaction, json_field_name)
        assert str(db_field) == json_field_value


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

        # check each field of requested json is equal to model field
        for json_field_name, json_field_value in requested_transaction.items():
            db_field = getattr(created_db_transaction, json_field_name)
            assert str(db_field) == json_field_value


@pytest.mark.django_db
@mock.patch('apps.wallet.serializers.validate_amount_signal_for_type', side_effect=Exception)
def test_serializer_validation_errors(mock) -> None:
    """
    Test serializer reassignments of ValidationError from validation errors
    """
    # get some transaction data to test
    transaction_to_create = sample_transactions_data()[0]

    # convert amount to negative or positive
    transaction_to_create['amount'] = str(-float(transaction_to_create['amount']))

    # check first scenery
    assert FinancialTransaction.objects.all().count() == 0

    # check serializer validations without failures
    serializer = FinancialTransactionSerializer(data=transaction_to_create)

    with pytest.raises(ValidationError) as exc:
        assert serializer.is_valid(raise_exception=True)
        if transaction_to_create['type'] == 'inflow':
            assert exc.messages[0] == error_messages['invalid_inflow_amount_value']
        elif transaction_to_create['type'] == 'outflow':
            assert exc.messages[0] == error_messages['invalid_outflow_amount_value']


@pytest.mark.django_db
def test_serializer_update_reference_ready_only_field(mock_db_transactions: Sequence[FinancialTransaction]) -> None:
    """
    Test reference field overwriting by payload
    """
    # get some requested transaction
    transaction_to_update = sample_transactions_data()[3]

    # check first scenery
    db_transaction = FinancialTransaction.objects.get(reference=transaction_to_update['reference'])

    # overwrite reference field
    transaction_to_update['reference'] = '999999'

    # check serializer validations without failures
    serializer = FinancialTransactionSerializer(db_transaction, data=transaction_to_update, partial=False)
    with pytest.raises(ValidationError):
        assert serializer.is_valid(raise_exception=True) is False
        assert serializer.errors['reference'][0][0] == 'reference is a read-only field'
