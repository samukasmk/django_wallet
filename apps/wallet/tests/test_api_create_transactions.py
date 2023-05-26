import pytest
from rest_framework import status
from rest_framework.test import APIClient
from apps.wallet.models import FinancialTransaction
from apps.wallet.tests.conftest import sample_transactions_data, normalize_dict_to_model


@pytest.mark.django_db
@pytest.mark.parametrize('transaction_to_create', sample_transactions_data())
def test_creation_single_valid_transactions(api_client: APIClient, transaction_to_create: dict) -> None:
    """
    Test endpoint to create transactions with valid data of each transaction
    """
    # make api request
    response = api_client.post('/transactions/', transaction_to_create)

    # check status code
    assert response.status_code == status.HTTP_201_CREATED

    # check objects creation on db
    transactions = FinancialTransaction.objects.all()
    assert transactions.count() == 1

    # check value assignments on objects fields
    created_db_transaction = transactions.first()
    assert created_db_transaction is not None

    # compare requests dict with existing model instance
    requested_transaction = normalize_dict_to_model(transaction_to_create)
    for field_name, field_value in requested_transaction.items():
        assert getattr(created_db_transaction, field_name) == field_value


@pytest.mark.django_db
def test_creation_bulk_valid_transactions(api_client: APIClient) -> None:
    """
    Test endpoint to create transactions with valid data of many transactions
    """
    transactions_to_create = sample_transactions_data()

    # make api request
    response = api_client.post('/transactions/', transactions_to_create)

    # check status code
    assert response.status_code == status.HTTP_201_CREATED

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
@pytest.mark.parametrize('transaction_to_create', sample_transactions_data())
def test_creation_single_transactions_invalid_signals(api_client: APIClient, transaction_to_create: dict) -> None:
    """
    Test endpoint to create transactions with invalid amount values of each transaction
    """
    # change amount value for invalid signal for transaction type
    transaction_to_create['amount'] = str(-float(transaction_to_create['amount']))

    # make api request
    response = api_client.post('/transactions/', transaction_to_create)

    # check status code
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # check error response
    assert 'amount' in response.data
    assert len(response.data['amount'])
    assert 'transactions can not have' in str(response.data['amount'][0])

    # check objects creation on db
    assert FinancialTransaction.objects.all().count() == 0


@pytest.mark.django_db
def test_creation_bulk_transactions_invalid_signals(api_client: APIClient) -> None:
    """
    Test endpoint to create transactions with invalid amount values of many transactions
    """
    transactions_to_create = sample_transactions_data()

    # change amount value for invalid signal for transaction type
    transactions_to_create[-1]['amount'] = str(-float(transactions_to_create[-1]['amount']))

    # make api request
    response = api_client.post('/transactions/', transactions_to_create)

    # check status code
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # check error response
    error_responses = [error_detail['amount']
                       for error_detail in response.data
                       if 'amount' in error_detail.keys()]
    assert len(error_responses)
    assert 'transactions can not have' in str(error_responses[0])

    # check objects creation on db
    assert FinancialTransaction.objects.all().count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize('transaction_to_create', sample_transactions_data())
def test_creation_single_transactions_invalid_type(api_client: APIClient, transaction_to_create: dict) -> None:
    """
    Test endpoint to create specific transaction with invalid transaction type
    """
    # change amount value for invalid signal for transaction type
    transaction_to_create['type'] = 'invalid'

    # make api request
    response = api_client.post('/transactions/', transaction_to_create)

    # check status code
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # check error response
    assert 'type' in response.data
    assert len(response.data['type'])
    assert 'is not a valid choice' in str(response.data['type'][0])

    # check objects creation on db
    assert FinancialTransaction.objects.all().count() == 0


@pytest.mark.django_db
def test_creation_bulk_transactions_invalid_type(api_client: APIClient) -> None:
    """
    Test endpoint to create many transactions with one invalid transaction type
    """
    transactions_to_create = sample_transactions_data()

    # change amount value for invalid signal for transaction type
    transactions_to_create[-1]['type'] = 'invalid_type'

    # make api request
    response = api_client.post('/transactions/', transactions_to_create)

    # check status code
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # check error response
    error_responses = [error_detail['type']
                       for error_detail in response.data
                       if 'type' in error_detail.keys()]
    assert len(error_responses)
    assert 'is not a valid choice' in str(error_responses[0])

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
    response = api_client.post('/transactions/', transaction_to_create)

    # check status code
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # check error response
    assert required_field in response.data
    assert len(response.data[required_field])
    assert 'This field is required' in str(response.data[required_field][0])

    # check objects creation on db
    assert FinancialTransaction.objects.all().count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize('required_field', ['reference', 'date', 'amount', 'type', 'category', 'user_email'])
@pytest.mark.parametrize('transaction_position_in_bulk', list(range(len(sample_transactions_data()))))
def test_creation_bulk_transactions_missing_required_fields(api_client: APIClient,
                                                            required_field: str,
                                                            transaction_position_in_bulk: int) -> None:
    """
    Test endpoint to create many transactions with one invalid transaction type
    """
    transactions_to_create = sample_transactions_data()

    # change amount value for invalid signal for transaction type
    transactions_to_create[transaction_position_in_bulk].pop(required_field, None)

    # make api request
    response = api_client.post('/transactions/', transactions_to_create)

    # check status code
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # check error response
    error_responses = [error_detail[required_field]
                       for error_detail in response.data
                       if required_field in error_detail.keys()]
    assert len(error_responses)
    assert 'This field is required' in str(error_responses[0])

    # check objects creation on db
    assert FinancialTransaction.objects.all().count() == 0
