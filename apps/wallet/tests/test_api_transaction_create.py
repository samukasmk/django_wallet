import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.wallet.models import FinancialTransaction
from apps.wallet.tests.conftest import sample_transactions_data


@pytest.mark.django_db
@pytest.mark.parametrize('transaction_to_create', sample_transactions_data())
def test_creation_single_valid_transactions(api_client: APIClient, transaction_to_create: dict) -> None:
    """
    Test endpoint to create transactions with valid data of each transaction
    """
    # make api request
    response = api_client.post('/transaction', transaction_to_create)

    # check status code
    assert response.status_code == status.HTTP_201_CREATED

    # check objects creation on db
    db_transactions = FinancialTransaction.objects.all()
    assert db_transactions.count() == 1

    # check value assignments on objects fields
    created_db_transaction = db_transactions.first()
    assert created_db_transaction is not None

    # compare requested json with existing model instance
    for json_field_name, json_field_value in transaction_to_create.items():
        db_field = getattr(created_db_transaction, json_field_name)
        assert str(db_field) == json_field_value


@pytest.mark.django_db
@pytest.mark.parametrize('transaction_to_create', sample_transactions_data())
def test_creation_single_transactions_invalid_type(api_client: APIClient, transaction_to_create: dict) -> None:
    """
    Test endpoint to create specific transaction with invalid transaction type
    """
    # change amount value for invalid signal for transaction type
    transaction_to_create['type'] = 'invalid'

    # make api request
    response = api_client.post('/transaction', transaction_to_create)

    # check status code
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # check error response
    response_dict = response.json()
    assert 'type' in response_dict
    assert len(response_dict['type'])
    assert response_dict['type'][0] == '"invalid" is not a valid choice.'

    # check objects creation on db
    assert FinancialTransaction.objects.all().count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize('transaction_to_create', sample_transactions_data())
def test_creation_single_transactions_invalid_amount_values(api_client: APIClient, transaction_to_create: dict) -> None:
    """
    Test endpoint to create transactions with invalid amount values of each transaction
    """
    # change amount value for invalid signal for transaction type
    transaction_to_create['amount'] = str(-float(transaction_to_create['amount']))

    # make api request
    response = api_client.post('/transaction', transaction_to_create)

    # check status code
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # check error response
    response_dict = response.json()
    assert 'amount' in response_dict
    assert len(response_dict['amount'])
    if transaction_to_create['type'] == 'inflow':
        assert response_dict['amount'][0] == ('Inflow transactions can not have negative values in '
                                              'the "amount" field, please provide a positive value.')
    elif transaction_to_create['type'] == 'outflow':
        assert response_dict['amount'][0] == ('Outflow transactions can not have positive values in '
                                              'the "amount" field, please provide a negative value.')

    # check objects creation on db
    assert FinancialTransaction.objects.all().count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize('transaction_to_create', sample_transactions_data())
def test_creation_single_transactions_invalid_value(api_client: APIClient, transaction_to_create: dict) -> None:
    """
    Test endpoint to create transactions with invalid amount values of each transaction
    """
    # change amount value for invalid signal for transaction type
    transaction_to_create['amount'] = '1.a'

    # make api request
    response = api_client.post('/transaction', transaction_to_create)

    # check status code
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # check error response
    response_dict = response.json()
    assert 'amount' in response_dict
    assert len(response_dict['amount'])
    assert response_dict['amount'][0] == 'A valid number is required.'

    # check objects creation on db
    assert FinancialTransaction.objects.all().count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize('transaction_to_create', sample_transactions_data())
@pytest.mark.parametrize('required_field', ['reference', 'date', 'amount', 'type', 'category', 'user_email'])
def test_creation_single_transactions_missing_required_fields(api_client: APIClient,
                                                              transaction_to_create: dict,
                                                              required_field: str) -> None:
    """
    Test endpoint to create specific transaction with invalid transaction type
    """
    # remove required field
    transaction_to_create.pop(required_field, None)

    # make api request
    response = api_client.post('/transaction', transaction_to_create)

    # check status code
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # check error response
    response_dict = response.json()
    assert required_field in response_dict
    assert len(response_dict[required_field])
    assert response_dict[required_field][0] == 'This field is required.'

    # check objects creation on db
    assert FinancialTransaction.objects.all().count() == 0
