import pytest
from rest_framework import status
from apps.wallet.models import FinancialTransaction
from apps.wallet.tests.conftest import sample_transactions_data


@pytest.mark.django_db
def test_delete_transactions(api_client, sample_transactions_models):
    """ Test endpoint to delete transactions """
    transactions_to_delete = sample_transactions_data()
    models_count = len(transactions_to_delete)

    # check models existence in db
    assert FinancialTransaction.objects.all().count() == models_count

    # delete each transaction on database one by one
    for transaction_to_delete in transactions_to_delete:
        # remove existent object of database from api
        response = api_client.delete(f'/transaction/{transaction_to_delete["reference"]}')
        assert response.status_code == status.HTTP_200_OK

        # decrease counter and check length in db
        models_count -= 1
        assert FinancialTransaction.objects.all().count() == models_count

    # final check on db
    assert FinancialTransaction.objects.all().count() == models_count
