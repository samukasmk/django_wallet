import pytest
from rest_framework import status
from apps.wallet.models import FinancialTransaction
from apps.wallet.tests.conftest import sample_transactions_data


@pytest.mark.django_db
def test_get_transactions(api_client, sample_transactions_models):
    """ Test endpoint to get a specific transaction """
    transactions_to_get = sample_transactions_data()

    # check models existence in db
    assert FinancialTransaction.objects.all().count() == len(transactions_to_get)

    # get each transaction on database one by one
    for transaction_to_get in transactions_to_get:

        # get existent object of database from api
        response = api_client.get(f'/transaction/{transaction_to_get["reference"]}')
        assert response.status_code == status.HTTP_200_OK
        assert response.data == transaction_to_get
