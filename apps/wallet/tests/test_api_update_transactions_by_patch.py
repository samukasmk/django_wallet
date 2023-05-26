import pytest
from typing import Sequence
from rest_framework import status
from rest_framework.test import APIClient
from apps.wallet.models import FinancialTransaction
from apps.wallet.tests.conftest import sample_transactions_data


@pytest.mark.django_db
def test_update_transactions_by_patch(api_client: APIClient,
                                      sample_transactions_models: Sequence[FinancialTransaction]) -> None:
    """ Test endpoint to update some specific information in a transaction """
    transactions_to_get = sample_transactions_data()

    # check models existence in db
    assert FinancialTransaction.objects.all().count() == len(transactions_to_get)

    # get each transaction on database one by one
    for transaction_to_get in transactions_to_get:
        amount_transaction = float(transaction_to_get["amount"])

        # ensure current amount is equal of request value in mock
        assert FinancialTransaction.objects.get(
            reference=transaction_to_get["reference"]).amount == amount_transaction

        # increase or decrease new amount to change
        if amount_transaction > 0:
            amount_transaction += 50000000.0
        elif amount_transaction < 0:
            amount_transaction -= 50000000.0

        # create partial payload to change data
        payload = {'amount': str(amount_transaction),
                   'category': 'updated_category_by_patch'}

        # get existent object of database from api
        response = api_client.patch(f'/transactions/{transaction_to_get["reference"]}/', payload)

        # check returned payload with updated data
        assert response.status_code == status.HTTP_200_OK
        assert response.data['reference'] == transaction_to_get["reference"]
        assert response.data['amount'] == str(amount_transaction)
        assert response.data['category'] == 'updated_category_by_patch'

        # check update on database
        assert FinancialTransaction.objects.get(
            reference=transaction_to_get["reference"]).amount == amount_transaction
        assert FinancialTransaction.objects.get(
            reference=transaction_to_get["category"]).amount == 'updated_category_by_patch'
