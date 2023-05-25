import pytest
from rest_framework import status
from apps.wallet.models import FinancialTransaction
from apps.wallet.tests.conftest import sample_transactions_data


@pytest.mark.django_db
def test_get_specific_transactions(api_client, sample_transactions_models):
    """ Test endpoint to get all transactions """
    transactions_to_get = sample_transactions_data()

    # check models existence in db
    assert FinancialTransaction.objects.all().count() == len(transactions_to_get)

    # get existent objects of database from api
    response = api_client.get('/transactions/')
    assert response == status.HTTP_200_OK
    assert response.data == transactions_to_get
