import pytest
from rest_framework import status
from apps.wallet.models import FinancialTransaction
from apps.wallet.tests.conftest import sample_transactions_data


@pytest.mark.django_db
@pytest.mark.parametrize('transaction_to_create', sample_transactions_data())
def test_creation_single_valid_transactions(api_client, transaction_to_create):
    """ Test POST requests with valid data of each transaction """
    # make api request
    response = api_client.post('/transactions', transaction_to_create)

    # check status code
    assert response.status_code == status.HTTP_201_CREATED

    # check objects creation on db
    transactions = FinancialTransaction.objects.all()
    assert transactions.count() == 1

    # check value assignments on objects fields
    created_transaction = transactions.first()
    assert created_transaction is not None

    for field_name, field_value in transaction_to_create.items():
        assert getattr(created_transaction, field_name) == field_value


@pytest.mark.django_db
def test_creation_bulk_valid_transactions(api_client):
    """ Test POST requests with valid data of many transactions """
    transactions_to_create = sample_transactions_data()

    # make api request
    response = api_client.post('/transactions', transactions_to_create)

    # check status code
    assert response.status_code == status.HTTP_201_CREATED

    # check objects creation on db
    db_transactions = FinancialTransaction.objects.all()
    assert db_transactions.count() == len(transactions_to_create)

    # check value assignments on objects fields
    for index_position, created_db_transaction in enumerate(db_transactions):
        # get requested dict
        requested_transaction = transactions_to_create[index_position]
        # check each field of requested dict is equal to model field
        for field_name, field_value in requested_transaction.items():
            assert getattr(created_db_transaction, field_name) == field_value


@pytest.mark.django_db
@pytest.mark.parametrize('transaction_to_create', sample_transactions_data())
def test_creation_single_invalid_transactions(api_client, transaction_to_create):
    """ Test POST requests with invalid amount values of each transaction """
    # change amount value for invalid signal for transaction type
    transaction_to_create['amount'] = str(-float(transaction_to_create['amount']))

    # make api request
    response = api_client.post('/transactions', transaction_to_create)

    # check status code
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # check objects creation on db
    assert FinancialTransaction.objects.all().count() == 0


@pytest.mark.django_db
def test_creation_bulk_invalid_transactions(api_client):
    """ Test POST requests with invalid amount values of many transactions """
    transactions_to_create = sample_transactions_data()

    # change amount value for invalid signal for transaction type
    transactions_to_create[-1]['amount'] = str(-float(transactions_to_create[-1]['amount']))

    # make api request
    response = api_client.post('/transactions', transactions_to_create)

    # check status code
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # check objects creation on db
    assert FinancialTransaction.objects.all().count() == 0
